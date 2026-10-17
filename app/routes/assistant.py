from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from app.services.assistant_service import AssistantService

assistant_bp = Blueprint('assistant', __name__)


@assistant_bp.route('/assistant')
def index():
    """Interactive Reading Atelier companion page."""
    return render_template('assistant/index.html')


@assistant_bp.route('/assistant/chat', methods=['POST'])
def chat():
    """Deterministic chat endpoint for assistant queries."""
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    user_id = current_user.id if current_user.is_authenticated else None

    response = AssistantService.process_query(user_id=user_id, message=message)
    return jsonify(response)
