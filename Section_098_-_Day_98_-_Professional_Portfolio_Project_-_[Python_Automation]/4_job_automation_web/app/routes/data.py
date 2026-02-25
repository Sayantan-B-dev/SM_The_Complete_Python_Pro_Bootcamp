from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import data_manager
import pandas as pd
import io

data_bp = Blueprint('data', __name__)

@data_bp.route('/')
def list_data():
    df = data_manager.read_data()
    # Convert to list of dicts for template
    records = df.to_dict('records')
    columns = df.columns.tolist()
    return render_template('data_list.html', records=records, columns=columns)

@data_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Build dict from form
        row = {key: request.form[key] for key in request.form}
        data_manager.add_row(row)
        flash('Row added successfully')
        return redirect(url_for('data.list_data'))
    # Get columns from existing data or default
    df = data_manager.read_data()
    columns = df.columns.tolist() if not df.empty else ['Name', 'Email', 'Department', 'Score']
    return render_template('data_add.html', columns=columns)

@data_bp.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    df = data_manager.read_data()
    if index >= len(df):
        flash('Row not found')
        return redirect(url_for('data.list_data'))
    if request.method == 'POST':
        row = {key: request.form[key] for key in request.form}
        data_manager.update_row(index, row)
        flash('Row updated successfully')
        return redirect(url_for('data.list_data'))
    # Get current row data
    row_data = df.iloc[index].to_dict()
    columns = df.columns.tolist()
    return render_template('data_edit.html', index=index, row=row_data, columns=columns)

@data_bp.route('/delete/<int:index>')
def delete(index):
    data_manager.delete_row(index)
    flash('Row deleted successfully')
    return redirect(url_for('data.list_data'))

@data_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Check if file upload or text paste
        if 'csv_file' in request.files and request.files['csv_file'].filename != '':
            file = request.files['csv_file']
            try:
                # Read uploaded file
                new_df = pd.read_csv(file)
            except Exception as e:
                flash(f'Error reading CSV file: {e}', 'danger')
                return redirect(url_for('data.upload'))
        elif 'csv_text' in request.form and request.form['csv_text'].strip() != '':
            csv_text = request.form['csv_text']
            try:
                # Read from text string
                new_df = pd.read_csv(io.StringIO(csv_text))
            except Exception as e:
                flash(f'Error parsing CSV text: {e}', 'danger')
                return redirect(url_for('data.upload'))
        else:
            flash('No data provided.', 'warning')
            return redirect(url_for('data.upload'))

        # Basic cleaning: strip whitespace from string columns
        for col in new_df.select_dtypes(include=['object']).columns:
            new_df[col] = new_df[col].str.strip()

        # Determine action: append or replace
        action = request.form.get('action', 'append')  # 'append' or 'replace'

        if action == 'replace':
            data_manager.write_data(new_df)
            flash(f'Replaced all data with {len(new_df)} rows.', 'success')
        else:
            # Append to existing data
            data_manager.append_data(new_df)
            flash(f'Appended {len(new_df)} rows to existing data.', 'success')

        return redirect(url_for('data.list_data'))

    # GET request: show upload form
    return render_template('data_upload.html')

@data_bp.route('/clear_all')
def clear_all():
    # Create empty DataFrame with default columns
    import pandas as pd
    from app.models.data_manager import DEFAULT_COLUMNS, write_data
    empty_df = pd.DataFrame(columns=DEFAULT_COLUMNS)
    write_data(empty_df)
    flash('All data cleared.', 'success')
    return redirect(url_for('data.list_data'))