from flask import Blueprint, jsonify
from blockchain.ledger import Blockchain

audit_bp = Blueprint('audit', __name__, url_prefix='/audit')
blockchain = Blockchain()

@audit_bp.route('/log', methods=['POST'])
def log_action():
    data = request.get_json()
    blockchain.add_block(data)
    return jsonify({"status": "logged", "block_index": len(blockchain.chain)-1})

@audit_bp.route('/verify')
def verify_chain():
    is_valid = blockchain.verify()
    return jsonify({"valid": is_valid, "length": len(blockchain.chain)})