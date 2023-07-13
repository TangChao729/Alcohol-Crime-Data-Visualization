from mpi4py import MPI
import json
#  mpiexec -n 5 python -m mpi4py main-postprocess.py
comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()
tweets = []
if comm_size != 5:
    print("Must run in a 5-processor environment!")
else:
    with open("output"+str(comm_rank)+".json", 'r') as data_file:
        json_data = data_file.read()
    data = json.loads(json_data)
    for d in data:
        includes = d["includes"]
        if type(includes) == type({}):
            places = includes["places"]
            place = places[0]
            full_name = place["full_name"]
            d_list = full_name.split(",")
            d_list = [i.strip().lower() for i in d_list]
            if "victoria" in d_list:
                tweets.append(d)
        else:
            place = includes[0]
            full_name = place["full_name"]
            d_list = full_name.split(",")
            d_list = [i.strip().lower() for i in d_list]
            if "victoria" in d_list:
                tweets.append(d)
print(comm_rank, len(tweets))
tweets_total = comm.gather(tweets, root=0)
if comm_rank == 0:
    tweets_list = [t for sub_tweets in tweets_total for t in sub_tweets]
    print(len(tweets_list))
    with open("output-vic.json", "w") as file:
        json.dump(tweets_list, file, indent=4)

# There are total 928015 tweets in huge dataset
