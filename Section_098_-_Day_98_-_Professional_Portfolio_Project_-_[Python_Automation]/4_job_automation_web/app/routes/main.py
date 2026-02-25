from flask import Blueprint, render_template
from app.models import data_manager, report_manager

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    input_df = data_manager.read_data()
    report_df = report_manager.read_report()
    return render_template('index.html',
                           input_rows=len(input_df),
                           input_cols=len(input_df.columns) if not input_df.empty else 0,
                           report_rows=len(report_df),
                           report_cols=len(report_df.columns) if not report_df.empty else 0)