import itertools

from django.test import TestCase, Client

from .models import User, Follower, Post, Likes


class UserTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create(username='TestUser1', email='test1@gmail.com', password='testing321')
        u2 = User.objects.create(username='TestUser2', email='test2@gmail.com', password='testing321')
        u3 = User.objects.create(username='TestUser3', email='test3@gmail.com', password='testing321')

    def test_unique_username(self):
        usernames = list(User.objects.all().values_list('username', flat=True))
        combinations = list(itertools.combinations(usernames, 2))
        for comb in combinations:
            self.assertNotEqual(comb[0], comb[1])


class FollowerTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create(username='TestUser1', email='test1@gmail.com', password='testing321')
        u2 = User.objects.create(username='TestUser2', email='test2@gmail.com', password='testing321')
        u3 = User.objects.create(username='TestUser3', email='test3@gmail.com', password='testing321')

        f1 = Follower.objects.create(follower_id=u1, following_id=u2)
        f2 = Follower.objects.create(follower_id=u1, following_id=u3)
        f3 = Follower.objects.create(follower_id=u3, following_id=u1)

    def test_1(self):
        followers = Follower.objects.all()
        for f in followers:
            self.assertNotEqual(f.follower_id.id, f.following_id.id)

    def test_2(self):
        u = User.objects.get(username='TestUser1')
        self.assertEqual(Follower.objects.filter(follower_id=u).count(), 2)

    def test_3(self):
        u = User.objects.get(username='TestUser1')
        self.assertEqual(Follower.objects.filter(following_id=u).count(), 1)

    def test_4(self):
        u = User.objects.get(username='TestUser2')
        self.assertEqual(Follower.objects.filter(follower_id=u).count(), 0)

    def test_5(self):
        u = User.objects.get(username='TestUser2')
        self.assertEqual(Follower.objects.filter(following_id=u).count(), 1)

    def test_6(self):
        u = User.objects.get(username='TestUser3')
        self.assertEqual(Follower.objects.filter(follower_id=u).count(), 1)

    def test_7(self):
        u = User.objects.get(username='TestUser3')
        self.assertEqual(Follower.objects.filter(following_id=u).count(), 1)


class LikesTestCase(TestCase):

    def setUp(self):
        u1 = User.objects.create(username='TestUser1', email='test1@gmail.com', password='testing321')
        u2 = User.objects.create(username='TestUser2', email='test2@gmail.com', password='testing321')
        u3 = User.objects.create(username='TestUser3', email='test3@gmail.com', password='testing321')

        p1 = Post.objects.create(author=u1, content='Test content1')
        p2 = Post.objects.create(author=u3, content='Test content2')
        p3 = Post.objects.create(author=u2, content='Test content3')
        p4 = Post.objects.create(author=u2, content='Test content4')
        p5 = Post.objects.create(author=u2, content='Test content5')
        p6 = Post.objects.create(author=u2, content='Test content6')

        l1 = Likes.objects.create(liked_post=p1, user=u1)
        l2 = Likes.objects.create(liked_post=p2, user=u2)
        l3 = Likes.objects.create(liked_post=p3, user=u3)
        l4 = Likes.objects.create(liked_post=p4, user=u3)
        l5 = Likes.objects.create(liked_post=p5, user=u2)
        l6 = Likes.objects.create(liked_post=p6, user=u1)

    def test_likes_count(self):
        # one user can add only 1 like to post
        likes = list(Likes.objects.all().values_list('liked_post_id', 'user_id'))
        combinations = list(itertools.combinations(likes, 2))
        for comb in combinations:
            self.assertNotEqual(comb[0], comb[1])

    def test_index(self):
        c = Client()
        response = c.get("/", )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object_list"].count(), 6)


class PostTestCase(TestCase):

    def setUp(self):
        u1 = User.objects.create(username='TestUser1', email='test1@gmail.com', password='testing321')
        u2 = User.objects.create(username='TestUser2', email='test2@gmail.com', password='testing321')
        u3 = User.objects.create(username='TestUser3', email='test3@gmail.com', password='testing321')

        p1 = Post.objects.create(author=u1,
                                 content='"Eggs are bursting with vitamins. Plus, they contain all nine essential amino acids (valine, leucine, isoleucine, histidine, lysine, methionine, tryptophan, phenylalanine, threonine). Eggs are very versatile, which makes them a must-have on your healthy shopping list. If you eat this high-protein food for lunch in a salad, you are pretty much guaranteed to avoid hunger cravings in the afternoon."')
        p2 = Post.objects.create(author=u3,
                                 content='"Onions and garlic belong to the genus Allium. A healthy, fresh diet is almost unimaginable without these two, as they are crucial for adding flavor to the food you eat.')
        p3 = Post.objects.create(author=u2,
                                 content='The arch rival of the mkdir command, the rmdir command allows you to delete specific folders from your system without any hassles. Although many utilize the rm command for this purpose, screwing up parameters or even a single character with rm can do things you wouldn’t even dream. So, stick with rmdir for now.')
        p4 = Post.objects.create(author=u2,
                                 content='Onions contain essential oils and sulphur-containing compounds (sulfides). This makes them not only an herb, but a medicinal plant too: Sulfides are phytonutrients, which are said to have many benefits for your body. If eaten regularly, they are supposed to lower your risk of cancer and protect you from bacterial diseases.(3) Sulfides are always present in garlic."')
        p5 = Post.objects.create(author=u2,
                                 content='pwd stands for Print Work directory and does exactly what you think – it shows the directory you’re currently in. This is one of the handiest Linux terminal commands that aims to make new user’s life peaceful by ensuring they don’t get lost in that seemingly cryptic terminal window.')
        p6 = Post.objects.create(author=u2,
                                 content='The ls command is probably one of the most widely used commands in the Unix world. It presents to you the contents of a particular directory – both files and directories. You will use this command alongside pwd to navigate your ways inside the mighty Unix filesystem.')

    def test_post_length(self):
        posts = Post.objects.all()
        for p in posts:
            self.assertGreater(len(p.content), 50)

    def test_2(self):
        u = User.objects.get(username='TestUser1')
        self.assertEqual(Post.objects.filter(author=u).count(), 1)

    def test_3(self):
        u = User.objects.get(username='TestUser2')
        self.assertEqual(Post.objects.filter(author=u).count(), 4)

    def test_4(self):
        u = User.objects.get(username='TestUser3')
        self.assertEqual(Post.objects.filter(author=u).count(), 1)

    def test_valid_post_page(self):
        u = User.objects.get(username='TestUser1')
        p = Post.objects.get(author=u)
        c = Client()
        response = c.get(f"/post_detail/{p.id}/")
        self.assertEqual(response.status_code, 200)

    def test_invalid_post_page(self):
        max_id = max(list(Post.objects.all().values_list('id', flat=True)))
        c = Client()
        response = c.get(f"/post_detail/{max_id + 1}/")
        self.assertEqual(response.status_code, 404)
