import praw
import random
import datetime
import time
import re
import reddit
from textblob import TextBlob

Trumps = ['Trump', 'President Trump', 'Donald Trump' , 'Orange', 'Donald J. Trump']
Americas = ['America', 'United States', 'USA', 'the US', 'United States of America']
greats = ['great', 'wonderful', 'powerful', 'awesome', 'fabulous']
celebrates = ['celebrate', 'congratulate', 'honor', 'commenmorate', 'acknowledge']
abolishs = ['abolish', 'destroy', 'delete', 'get rid of', 'put an end to']
Bidens = ['Joe Biden', 'Biden', 'Joe', 'Sleepy Joe', 'Democrats']

def generate_comment_0():
    Trump = random.choice(Trumps)
    America = random.choice(Americas)
    great = random.choice(greats)
    abolish = random.choice(abolishs)
    Biden = random.choice(Bidens)

    text = Trump + ''' does not have a dog. He is anti-dog and anti-''' + America + '''. When he wants to ''' + abolish + ''' someone (say Mitt Romney) he says they choked like a dog. Or in the case of a ''' + great + ''' woman (say Carly Fiorina) he says they have a face like a dog. ''' + Biden + ''' loves dog though.'''
    return text

def generate_comment_1():
    Trump = random.choice(Trumps)
    America = random.choice(Americas)
    great = random.choice(greats)
    celebrate = random.choice(celebrates)
    Biden = random.choice(Bidens)

    text = Trump + ''' has no sense of humor. He does not tell ''' + great + ''' funny stories, and he does not ''' + celebrate + ''' ''' + America + ''' ever. His idea of wit is to imitate people with afflictions, or give you a 5th grade nickname like Little Marco or Nervous ''' + Biden + '''.'''
    return text

def generate_comment_2():
    Trump = random.choice(Trumps)
    America = random.choice(Americas)
    great = random.choice(greats)
    abolish = random.choice(abolishs)
    Biden = random.choice(Bidens)

    text = Trump + ''' is such a whiner of ''' + America + '''. You would think a guy in the White House, with the Senate in his lap, two of his own Supreme Court Justices and Fox News would have things under ''' + great + ''' control. But he ''' + abolish + ''' everything and plays the victim card like Blanche DuBois. ''' + Biden + ''' never does that.'''
    return text

def generate_comment():
    functions = [generate_comment_0(), generate_comment_1(), generate_comment_2()]
    text = random.choice(functions)
    return text

def cs40_exception_handling(exception):
    print(exception)
    if exception == praw.exceptions.APIException:
        return True
    return False

def cs40_blindUpvote(text):
    # Extra 1, Extra 2
    dem_regex = re.findall(r'biden|democrat\w*|vice president',text, re.IGNORECASE)
    if dem_regex != []:
        return True
    return False

def cs40_sentiment_analysis(text):
    # Extra 8
    dem_regex = re.findall(r'biden|democrat\w*|vice president',text, re.IGNORECASE)
    rep_regex = re.findall(r'trump|republican\w*|president', text, re.IGNORECASE)
    blob = TextBlob(text).sentiment.polarity
    # sentimental analysis
    if dem_regex != []:
        if blob > 0:
            return True
        elif blob < 0:
            return False
        return None
    if rep_regex != []:
        if blob < 0:
            return True
        elif blob > 0:
            return False
        return None
    return None

def cs40_Upvote_Submission(submission):
    # Extra 8
    title = submission.title
    if cs40_sentiment_analysis(title) == True:
        submission.upvote()
        print('SUBMISSION Upvoted:', title)
    if cs40_sentiment_analysis(title) == False:
        submission.downvote()
        print('SUBMISSION Downvoted:', title)
    return

def cs40_Upvote_Comment(comment):
    # Extra 8
    content = comment.body
    if cs40_sentiment_analysis(content) == True:
        comment.upvote()
        print('COMMENT Upvoted:', content)
    if cs40_sentiment_analysis(content) == False:
        comment.downvote()
        print('COMMENT Downvoted:', content)
    return

def cs40_Post_Submission(subreddit):
    # Extra 6
    print('Posting Submissions...........')
    politic_submissions = list(reddit.subreddit('politics').new(limit=None))
    politic_submission = random.choice(politic_submissions)
    politic_submission.comments.replace_more(limit=None)
    s = "Done Submission"
    try:
        subreddit.submit("From Hoang's bot_1: " + politic_submission.title, url=politic_submission.url)
    except Exception as exception:
        if cs40_exception_handling(exception):
            return s
        else:
            pass
    else:
        print('Submitted!')
    time.sleep(5)
    return s

def cs40_bot_army():
    # Extra 7
    bots = []
    for i in range(2,31):
        bot_name = 'bot_' + str(i)
        bots.append(bot_name)
    for bot in bots:
        print("From " + bot + ":")
        reddit = praw.Reddit(bot)
        reddit.validate_on_submit = True
        submissions = list(reddit.redditor("EaseAny").submissions.new(limit=None))
        for submission in submissions:
            # Extra 2
            title = submission.title
            if cs40_blindUpvote(title):
                submission.upvote()
            cs40_Upvote_Submission(submission)
        submission.comments.replace_more(limit=None)
        comments = list(reddit.redditor('EaseAny').comments.new(limit=None))
        for comment in comments:
            # Extra 1
            content = comment.body
            if cs40_blindUpvote(content):
                comment.upvote()
            comment.refresh()
            cs40_Upvote_Comment(comment)
            comment.refresh()
    print("We are done!")
    return

def cs40_task_5(subreddit):
    submission = None 
    debate_url = 'https://www.reddit.com/r/csci040temp/comments/jhb20w/2020_debate_thread/'
    rand_num = 0.6
    # rand_num = random.random()
    if rand_num < 0.5:
        submission = reddit.submission(url=debate_url)
    else:
        submissions = list(subreddit.top('all'))
        submission = random.choice(submissions)
    return submission

def cs40_task_4(submission, comments_without_replies):
    # Extra 3
    comments_without_replies = sorted(comments_without_replies, key=lambda comment: comment.score, reverse=True)
    for comment in comments_without_replies:
        # Extra 9
        text = None
        if cs40_sentiment_analysis(comment.body) == False: # Trump's great
            text = "This is Hoang's bot_1: " + generate_comment()
        elif cs40_sentiment_analysis(comment.body) == True:   # Trump sucks
            text = "This is Hoang's bot_1. Trump indeed sucks. He acts more like a communist than a normal person."
        else:
            text = "This is Hoang's bot_1. Don't forget to vote for Biden. Let's Build Back Better!"
        try:
            comment.reply(text)
        except Exception as exception:
            if cs40_exception_handling(exception):
                return
            else:
                pass
        else:
            print("Replied comment:", comment)
        time.sleep(5)
    return

def cs40_task_3(not_my_comments):
    comments_without_replies = []
    count = 0
    for comment in not_my_comments:
        try:
            replies = comment.replies
        except Exception:
            comments_without_replies.append(comment)
        else:
            for reply in replies:
                # print('reply=', reply.body)
                if reply.author == reddit.config.username:
                    count += 1
                else:
                    parent = reply.parent()
                    if parent is not praw.models.Submission:
                        if parent.author == reddit.config.username:
                            count += 1
            if count == 0:
                comments_without_replies.append(comment)
            count = 0
    print('comments_without_replies', len(comments_without_replies))
    return comments_without_replies

def cs40_task_2(all_comments, not_my_comments):
    has_not_commented = len(not_my_comments) == len(all_comments)
    # print('has_not_commented=',has_not_commented)
    return has_not_commented

def cs40_task_1(all_comments):
    not_my_comments = []
    for comment in all_comments:
        if comment.author != reddit.config.username:
            not_my_comments.append(comment)
    # print('not_my_comments=', len(not_my_comments))
    return not_my_comments

def cs40_task_0(submission):
    submission.comments.replace_more(limit=None)
    all_comments = []
    for comment in submission.comments.list():
        all_comments.append(comment)
    # print('len(all_comments)=',len(all_comments))
    return all_comments

def cs40_sub_task(has_not_commented, submission):
    if has_not_commented:
        top_level_comment = "This is Hoang's bot_1. Vote Biden. Let's Build Back Better."
        try:
            submission.reply(top_level_comment)
        except Exception as exception:
            if cs40_exception_handling(exception):
                time.sleep(5)
            else:
                pass
    return

def cs40_Reply_All(subreddit):

    # FIXME (task 5): select a new submission for the next iteration;
    # your newly selected submission should have a 50% chance of being the original submission
    # (url in the reddit_debate_url variable)
    # and a 50% chance of being randomly selected from the top submissions to the csci040 subreddit for the past month
    submission = cs40_task_5(subreddit)
    print('Starting to reply...........')
    print()
    print('new iteration at:',datetime.datetime.now())
    print('submission.title=',submission.title)
    print('submission.url=',submission.url)

    # Upvote Submissions
    cs40_Upvote_Submission(submission)
    print('finished 1')
    # FIXME (task 0): get a list of all of the comments in the submission
    all_comments = cs40_task_0(submission)
    print('finished 2')
    # FIXME (task 1): filter all_comments to remove comments that were generated by your bot
    not_my_comments = cs40_task_1(all_comments)
    print('finished 3')
    # FIXME (task 2)
    # if you have not made any comment in the thread, then post a top level comment
    has_not_commented = cs40_task_2(all_comments, not_my_comments)
    cs40_sub_task(has_not_commented, submission)
    print('finished 4')
    # FIXME (task 3): filter the not_my_comments list to also remove comments that 
    # you've already replied to
    comments_without_replies = cs40_task_3(not_my_comments)
    print('finished 5')
    # FIXME (task 4): randomly select a comment from the comments_without_replies list,
    # and reply to that comment
    cs40_task_4(submission, comments_without_replies)
    print('finished 6')
    # total = 0
    # for submission in reddit.redditor('EaseAny').submissions.new(limit=None):
    #     total += submission.num_comments
    # return total

def cs40_Enter_Subreddit(reddit):
    # connect to the debate thread
    print('Entering cs40...........')
    try:
        subreddit = reddit.subreddit('csci040temp')
    except Exception:
        print('Exception found')
        return
    else:
        print('Entered cs40')
    return subreddit

def main(reddit):
    subreddit = cs40_Enter_Subreddit(reddit)
    reddit.validate_on_submit = True
    while True:
        # Extra 4, Extra 5
        cs40_Reply_All(subreddit)
# main
if __name__ == "__main__":
    reddit = praw.Reddit('bot_1')
    main(reddit)




    





