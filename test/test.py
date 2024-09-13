import openai
import requests
import json
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# OpenAI API 설정
openai.api_key = "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"

async def get_food_info(food_name):
    return True
#async def get_foods_list(disease, allergy, vegan):
    # 사용자의 질병, 알레르기, 비건 여부에 따라 음식 리스트 반환 코드
    # 예를 들어, 비건이면 비건 식단을, 알레르기가 있다면 알레르기에 주의해야 하는 식단을 추천할 수 있습니다.
@app.route('/ai/recommend_food', methods=['POST'])
async def recommend_food():

    response_data = {
        'recommended_foods': "한글깨짐 테스트"
    }

    result = json.dumps(response_data, ensure_ascii=False)
    res = make_response(result)
    return res

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)