from pydoc import doc
import collections
import dataclasses
import textwrap
import redis

import hiredis 

# Necessary quart imports
from quart import Quart, g, request, abort
from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request

app = Quart(__name__)
QuartSchema(app)

# Initialize redis client
redisClient = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# delete everything in the redis client for testing
redisClient.flushall()

# Create a data class to assist with API data
@dataclasses.dataclass
class LeaderboardInfo:
    """ Contains details for a leaderboard. """
    username: str
    score: int

# Results posting endpoint
# Note: validate_request takes a param that is the data class just created
@app.route("/results/", methods=["POST"])
@validate_request(LeaderboardInfo)
async def postResults(data: LeaderboardInfo):
    """
    This function is responsible for posting the results of a game
    As it is not yet tied to the actual game, it currently takes in any values

    @return: 200 if successful
    Potential: May return 401 if data does not match the LeaderboardInfo dataclass template
    """

    # Create sorted set
    leaderboardSet = "Leaderboard"
    leaderboardData = dataclasses.asdict(data)

    # Initializing redis with members and values
    redisClient.zadd(leaderboardSet, {'Won in 1 guess': 25, 'Won in 2 guesses': 11, 'Won in 3 guesses': 20, 'Won in 4 guesses': 16, 'Won in 5 guesses': 19, 'Won in 6 guesses': 43, 'Lost': 10})

    #if result = 1 then dataset that is added is new
    #if result = 0 then dataset wasn't added because duplicate 
    result = redisClient.zadd(leaderboardSet, {leaderboardData["username"]: leaderboardData["score"]})
    resultOne = redisClient.zrange(leaderboardSet, 0, -1, desc = True, withscores = True, score_cast_func=int)

    if result == 0:
        return dict(resultOne), 200
    elif result != int:
        return {"Error:" "Something went wrong."}, 404


# top 10 scores endpoint
@app.route("/top-scores/", methods=["GET"])
async def topScores():
    """
    this function is responsible for retrieving the top 10 scores from the database

    @return: 200 if successful, 404 if not found
    """

    leaderboardSet = "Leaderboard"
    

    topScores = redisClient.zrange(leaderboardSet, 0, 9, desc = True, withscores = True)
    print(redisClient.zrange(leaderboardSet, 0, 9, desc = True, withscores = True))

    # Does the database have any data?
    if topScores != None:
        # If so, retrieve
        #data = dataclasses.asdict(topScores)
        return ('\n'.join(map(str, topScores))), 200
    else:
        # Should equal nil, or None, so return a message
        return {"Error": "Database empty."}, 404
