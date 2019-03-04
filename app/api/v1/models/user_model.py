
profile = []
class User(object):
    """ user data model to store data """

    def __init__(self):
        self.profile = profile
    
    def create_profile(self,data):
        profile = {
            'user_id' : len(self.profile) + 1,
            'username' : data['username'],
            'telephone' : data['telephone'],
            'passportUrl' : data['passportUrl'],
            'school_level' : data['school_level'],
            'status' : data['status']
        }

        self.profile.append(profile)
        return profile
    
    def get_specific_profile(self,id):

        """ Fetch a single profile by its ID """

        profile = [task for task in self.profile if task['user_id'] == id]

        return profile
    
    def get_profiles(self):

        """ Get all the registered profiles """

        return self.profile

    
    def update_profile(self,user_id, data):

        """ Update a profile by id """
        profile = [task for task in self.profile if task['user_id'] == user_id]

        profile[0]['user_id'] = user_id
        profile[0]['username'] = data['username']
        profile[0]['telephone'] = data['telephone']
        profile[0]['passportUrl'] = data['passportUrl']
        profile[0]['school_level'] = data['school_level']
        profile[0]['status'] = data['status']

        return profile
    
    def delete_profile(self, id):

        """ Delete a profile by ID """
        
        profile = [task for task in self.profile if task['user_id'] == id]

        self.profile.remove(profile[0])

        return profile