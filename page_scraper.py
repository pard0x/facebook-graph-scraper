import urllib2
import datetime
import json
import sqlite3 as lite
from optparse import OptionParser


class KEY:
    def __init__(key):
        self.key = None
        if not key:
            f = open('fb.key', 'r')
        else:
            f = open(key, 'r')
        self.key = key
    def get():
        return self.key

class DB:
    # This constructor will take a dict of configuration
    # if no db exists it will be created and ask for creds...
    def __init__(self, conf):
        self.con = None
        self.cur = None
        self.db_name = conf["db_name"]
        if not os.path.exists(db_name):
            print "Database does not exist, create one?"
            a = raw_input("Database does not exist, create one? (Y/n)"
            if not a.lower() == "n":
                f = open(db_name, 'w')
            else:
                print "Ok, you don't cooperate, I understand."
                print "[Error] Database option chosen, but refused."
                exit(1)
        con = lite.connect(db_name)
    
    # Save the data in DB
    # I can separate it by targets or write just to execute the query
    # For now it will be a query for simplicity
    def save(query):
        cur.execute(query)
        cur.commit()
    
    # Here we will close connection, encrypt the file
    # close it, and clear variables.
    def close():
        pass
        



# I don't have a key for facebook API yet, as soon as I'll have one with par on
# it, I will continue working on this script
def create_post_url(graph_url, APP_ID, APP_SECRET):
    # create the POST URL for Facebook API, posts can be changed with likes end more, have to check it
    post_args = "/posts/?key=value&access_token="+APP_ID+"|"+APP_SECRET
    post_url = graph_url + post_args
    
    return post_url

def create_comments_url(graph_url, post_id, APP_ID, APP_SECRET):
    comments_args = post_id + "/comments/?key=value&access_token="+API_ID+"|"+APP_SECRET
    comments_url = graph_url+comments_args
    
    return comments_url
    
def get_comments_data(comments_url, comment_data, post_id):
    #render URL to JSON
    comments = render_to_json(comments_url)["data"]
    #for each comment capture data
    for comment in comments:
        try:
            current_comments = [comment["id"], comment["message"], comment["like_count"],
                        comment["created_time"], post_id]
            comment_data.append(current_comments)
        except Exception:
            current_comments = ["error", "error", "error", "error", "error"]
    # check if there is another page
    try:
        # extract next page
        next_page = comments["paging"]["next"]
    except Exception:
        next_page = None
    
    # if we have another page, recurse
    if next_page is not None:
        get_comments_data(next_page, comment_data, post_id)
    else:
        return comment_data
        
    
def render_to_json(graph_url):
    res = urllib2.urlopen(graph_url)
    red = res.read()
    json_data = json.loads(red)
    
    return json_data
    
def scrape_posts_by_date(graph_url, date, post_data, APP_ID, APP_SECRET):
    page_posts = render_to_json(graph_url)
    next_page = page_posts["paging"]["next"]
    page_posts = page_posts["data"]
    collecting = True
    for post in page_posts:
        try:
            likes_count = get_likes_count(post["id"], APP_ID, APP_SECRET)
            current_post = [post["id"], post["message"], likes_count, post["created_time"],
                            post["shares"]["count"]]
        except Exception:
            current_post = ["error", "error", "error", "error"]
        if current_post[3] != "error":
            #compare data
            print date
            print current_post[3]
            if date <= current_post[3]:
                post_data.append(current_post)
            elif date > current_post[3]:
                print "Done Colecting"
                collecting = False
                break
    if collecting == True:
        scrape_posts_by_date(next_page, date, post_data, APP_ID, APP_SECRET)
    return post_data
    
def get_likes_count(post_id, APP_ID, APP_SECRET):
    graph_url = "https://graph.facebook.com/"
    likes_args = post_id + "/likes?summary=true&key=value&access_token"+APP_ID+"|"+APP_SECRET
    likes_url = graph_url + likes_args
    likes_json = render_to_json(likes_url)
    
    #pick out the likes count
    count_likes = likes_json["summary"]["total_count"]
    
    return count_likes

def main():
    parser = OptionParser()
    parser.add_option("-d", "--database", action="store", dest="database", 
                      type="string", help="save output to DB")
    
    (options, args) = parser.parse_args()
    
    # list of pages => the end of URL
    list_pages = ["AkbInternetSolutions", "ALDI.USA", "pythonlang"]
    graph_url = "http://graph.facebook.com/"
    
    last_crawl = datetime.datetime.now() - datetime.timedelta(weeks=1)
    last_crawl = last_crawl.isoformat()
    
    if options.database:
        pass
        
    # with API key for more data
    post_url = create_post_url(current, APP_ID, APP_SECRET)    
    
#    json_post = render_to_json(post_url)
#    json_fbposts = json_post['data]

    post_data = []
    post_data = scrape_posts_by_date(post_url, last_crawl, post_data)
    
    #print json_fbposts
    for post in fb_posts:
        try:
            print post["id"]
            print post["message"]
        except Exception:
            print "Error reading post"
    
    for page in list_pages:
        current = graph_url + page
        webresponse = urllib2.urlopen(current)
        readable_page = webresponse.read()
        json_page = json.loads(readable_page)
        
        print "----------" + page + "----------"
        print json_page["id"]
        print json_page["likes"]
        print json_page["talking_about_count"]
        print json_page["username"]
        print ''
        
        
if __name__ == "__main__":
    main()
