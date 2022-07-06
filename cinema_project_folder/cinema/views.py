from django.shortcuts import render


# Each request that has an efect on the database will send
# back to the frontend what had he done
# Operation      Data sent
# add            added object
# delete         deleted object
# update         {'prevdata': ObjBeforeUpdate, 'postdata': ObjAfterUpdate}
#
# When we have a multiple add, delete, or update a list of modified objects
# is sent

def index(request, *args, **kwargs):
    return render(request, 'index.html')
