user: hypercorn user --reload --debug --bind user.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
leaderboard: hypercorn leaderboard --reload --debug --bind leaderboard.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
primary: bin/litefs -config ./etc/primary.yml
secondaryOne: bin/litefs -config ./etc/secondaryOne.yml
secondaryTwo: bin/litefs -config ./etc/secondaryTwo.yml
