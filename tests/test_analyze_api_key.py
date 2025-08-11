import sys
import pathlib
import pytest
from fastapi.testclient import TestClient

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "server"))

import server.main as main

client = TestClient(main.app)

def test_analyze_without_api_key():
    """Test analyze endpoint without custom API key (should use server default)"""
    payload = {
        "result": {
            "winner": "attacker",
            "rounds": 5,
            "attacker_win_rate": 0.8,
            "defender_win_rate": 0.2
        }
    }
    
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    assert "analysis" in response.json()
    
    # Should return AI analysis when no API key is provided (uses server default)
    analysis = response.json()["analysis"]
    assert "attacker won" in analysis.lower()
    assert "80.0%" in analysis

def test_analyze_with_custom_api_key():
    """Test analyze endpoint with custom API key"""
    payload = {
        "result": {
            "winner": "defender",
            "rounds": 3,
            "attacker_win_rate": 0.3,
            "defender_win_rate": 0.7
        },
        "openai_api_key": "sk-test123456789"
    }
    
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    assert "analysis" in response.json()
    
    # Should return AI analysis when custom API key is provided
    analysis = response.json()["analysis"]
    assert "winner: defender" in analysis.lower()
    assert "70.0%" in analysis

def test_analyze_with_empty_api_key():
    """Test analyze endpoint with empty API key (should use server default)"""
    payload = {
        "result": {
            "winner": "attacker",
            "rounds": 4,
            "attacker_win_rate": 0.6,
            "defender_win_rate": 0.4
        },
        "openai_api_key": ""
    }
    
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    assert "analysis" in response.json()
    
    # Should return AI analysis when empty API key is provided (uses server default)
    analysis = response.json()["analysis"]
    assert "attacker won" in analysis.lower()
    assert "60.0%" in analysis

def test_analyze_with_whitespace_api_key():
    """Test analyze endpoint with whitespace-only API key (should use server default)"""
    payload = {
        "result": {
            "winner": "defender",
            "rounds": 6,
            "attacker_win_rate": 0.4,
            "defender_win_rate": 0.6
        },
        "openai_api_key": "   "
    }
    
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    assert "analysis" in response.json()
    
    # Should return AI analysis when whitespace-only API key is provided (uses server default)
    analysis = response.json()["analysis"]
    assert "winner: defender" in analysis.lower()
    assert "60.0%" in analysis
