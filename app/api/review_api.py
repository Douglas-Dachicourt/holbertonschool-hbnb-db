from flask import Blueprint, jsonify, request
from models.review import Review
from persistence.datamanager import DataManager
import json
review_api = Blueprint("review_api", __name__)
datamanager = DataManager(flag=4)


@review_api.route("/places/<string:id>/reviews", methods=["POST", "GET"])
def handle_place_review(id):
    """
    Function used to create and retriew reviews of a place
    """
    if request.method == "POST":
        place_id = id
        review_data = request.get_json()
        if not review_data:
            return jsonify({"Error": "Problem during review creation"}), 400

        rating = review_data.get("rating")
        if not isinstance(rating, int):
            return jsonify({"Error": "rating must be an integer."}), 400
        if not 1 <= rating <= 5:
            return jsonify({"Error":
                            "rating must be included between 1 and 5."}), 400

        comment = review_data.get("comment")
        if not isinstance(comment, str):
            return jsonify({"Error": "comment must be a string."}), 400

        try:
            with open("/home/hbnb/hbnb_data/User.json", 'r', encoding='UTF-8') as f:
                users = json.load(f)
            user_id = review_data.get("user_id")
            user_found = False
            for user in users:
                if user.get("uniq_id") == user_id:
                    user_found = True
                    break
            if not user_found:
                return jsonify({"Error": "User not found"}), 404
        except Exception as e:
            return jsonify({"Error": str(e)}), 404

        try:
            with open("/home/hbnb/hbnb_data/Place.json", 'r', encoding='UTF-8') as f:
                hosts = json.load(f)
            for host in hosts:
                if host.get("host_id") == user_id:
                    return jsonify({"Error": "Can't rate your own place"}), 400
        except Exception as e:
            return jsonify({"Error": str(e)}), 404


        try:
            with open("/home/hbnb/hbnb_data/Review.json", 'r', encoding='UTF-8') as f:
                reviews = json.load(f)
            for review in reviews:
                if review.get("user_id") == user_id \
                    and review.get("place_id") == place_id:
                        return jsonify({"Error":
                                    "Can't comment a same place twice"}), 400
        except Exception as e:
            return jsonify({"Error": str(e)}), 404


        if not all([user_id, place_id, rating, comment]):
            return jsonify({"Error": "Missing recquired field"}), 409

        new_review = Review(user_id, place_id, rating, comment)
        if not new_review:
            return jsonify({"Error": "adding new review"}), 500
        else:
            datamanager.save(new_review.to_dict())
            return jsonify({"Success": "Review added"}), 201

    else:
        try:
            with open("/home/hbnb/hbnb_data/Review.json", 'r', encoding='UTF-8') as f:
                reviews = json.load(f)
                return jsonify(reviews), 200
        except FileNotFoundError:
            return jsonify({"Error": "Review not found"}), 404


@review_api.route("/users/<string:id>/reviews", methods=['GET'])
def user_review(id):
    """
    Function that retrieves all reviews of a specific user
    """
    user_id = id
    try:
        with open("/home/hbnb/hbnb_data/Review.json", 'r', encoding='UTF-8') as f:
            reviews = json.load(f)
        for review in reviews:
            if review.get("user_id") == user_id:
                return jsonify(reviews), 200
    except FileNotFoundError:
        return jsonify({"Error": "Review not found"}), 404
    except Exception as e:
        return jsonify({"Error": str(e)})


@review_api.route("/reviews/<string:id>", methods=['GET', 'PUT', 'DELETE'])
def review_info(id):
    """
    Function that retrieves, updates and deletes a specific review
    """
    review_id = id
    if request.method == "GET":
        reviews = datamanager.get("Reviews", review_id)
        if not reviews:
            return jsonify({"Error": "Review not found"}), 404
        return jsonify(reviews), 200

    if request.method == "PUT":
        review_data = request.get_json()
        review = datamanager.get("Review", id)
        if not review:
            return jsonify({"Error": "Review not found"}), 404
        review["rating"] = review_data["rating"]
        review["comment"] = review_data["comment"]
        datamanager.update(review, id)
        return jsonify({"Success": "Review updated"}), 200

    if request.method == "DELETE":
        reviews = datamanager.get("Review", id)
        if not reviews:
            return jsonify({"Error": "Review not found"}), 404
        reviews = datamanager.delete("Reviews", id)
        if not reviews:
            return jsonify({"Success": "Review deleted"}), 200
