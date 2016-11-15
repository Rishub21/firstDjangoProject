import webhose

webhose.config(token="ce676c6c-02c7-47f4-a4e3-6f332774a976")
for post in webhose.search("github"):
    print(post.title)
