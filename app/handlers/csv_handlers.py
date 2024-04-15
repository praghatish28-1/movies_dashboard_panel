from flask import render_template, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
import os
import datetime
from app import celery
import logging
from app.movies.movies_fetcher import MoviesFetcher
from .csv_processor import CSVProcessor
from .db_manager import DBManager

logger = logging.getLogger(__name__)

class RouteHandler:
    def __init__(self, app):
        self.app = app
        self.uploads_db_manager = DBManager('uploads')
        self.movies_db_manager = DBManager('movies')

    def movies(self):
        if 'username' not in session:
            logger.warning("Attempt to access movies without login.")
            return redirect(url_for('login'))

        page = request.args.get('page', 1, type=int)
        sort_by = request.args.get('sort_by', 'date_added')
        sort_order = request.args.get('sort_order', 'asc')

        fetcher = MoviesFetcher(page=page, sort_by=sort_by, sort_order=sort_order)
        movies_list, total_pages = fetcher.fetch_movies()
        return movies_list, page, total_pages, sort_by, sort_order
    def upload_csv(self):
        file = request.files['file']
        filename = secure_filename(file.filename)
        current_working_directory = os.getcwd()
        upload_folder = self.app.config['UPLOAD_FOLDER']
        full_path = os.path.join(current_working_directory, upload_folder)
        filepath = os.path.join(full_path, filename)
        username = session.get('username', 'Anonymous')
        cron_id = int(datetime.datetime.now().timestamp() * 1000)

        try:
            if file and file.filename.endswith('.csv'):
                file.save(filepath)
                self.uploads_db_manager.insert_one({
                    'cron_id': cron_id,
                    'filename': filename,
                    'filepath': filepath,
                    'status': 'Uploaded',
                    'username': username,
                    'remark': "CSV upload started"
                })
                self.process_csv_task.delay(cron_id, filepath)
                return jsonify({'message': 'CSV upload started.'}), 202
            else:
                raise ValueError('Invalid file format')
        except Exception as e:
            logger.error(f"Error during CSV upload: {e}", exc_info=True)
            return jsonify({'error': str(e)}), 400

    def view_uploads(self):
        username = session.get('username')
        if not username:
            logger.warning("Unauthorized access attempt to view uploads.")
            return redirect(url_for('auth.login'))
        uploads = self.uploads_db_manager.find({'username': username})
        return uploads

    @celery.task(bind=True)
    def process_csv_task(self, cron_id, filepath):
        batch_size = 500
        csv_processor = CSVProcessor(filepath)
        movies_db_manager = DBManager('movies')
        uploads_db_manager = DBManager('uploads')
        try:
            uploads_db_manager.update_status(cron_id, 'In-progress', 'Adding to db')
            for batch in csv_processor.read_csv(batch_size):
                movies_db_manager.insert_batch(batch)
            uploads_db_manager.update_status(cron_id, 'Completed', 'Added successfully')
        except Exception as e:
            uploads_db_manager.update_status(cron_id, 'Failed', str(e))
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
