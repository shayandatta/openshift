from firebase import firebase

#FIREBASE_URL = "https://test-project-f8976.firebaseio.com/"


class FirebaseUtility:

    def __init__(self,firebaseauth):      
        self.fb = firebase.FirebaseApplication(firebaseauth['FIREBASE_URL'], None) 


    def insertdata(self,userid,indice,data):
        result = self.fb.patch('/{0}/{1}'.format(userid,indice),data)
        return result

#print(FirebaseUtility().insertdata('Shayan-test',{'A':1,'B':5,'C':3}))
