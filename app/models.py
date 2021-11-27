from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class DeckThema(models.Model):
    """デッキテーマ"""
    tier_num = (0, 1, 2, 3, 4)
    name = models.CharField(max_length=100) #?テーマ名
    tier = models.IntegerField(blank=True)
    in_played = models.IntegerField(default=0) #?何回使われたか
    win = models.IntegerField(default=0) #?勝ち数
    lose = models.IntegerField(default=0) #?負け数
    image = models.ImageField(blank=True) #?アイコン

    def __str__(self):
        return self.name

class Match(models.Model):
    """試合一覧"""
    player1 = models.ForeignKey(get_user_model(),related_name='player1', on_delete=models.PROTECT, blank=True)
    player2 = models.ForeignKey(get_user_model(),related_name='player2', on_delete=models.PROTECT)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # date_time = self.date + date_time.timedelta(hours=9)
        return  self.date.strftime("%m/%d %H:%M") + "\t" + str(self.player1) + "\tVS\t" + str(self.player2)


class Skill(models.Model):
    """スキル一覧"""
    skill_name = models.CharField(max_length=20)

    def __str__(self):
        return self.skill_name



class Result(models.Model):
    """試合結果"""
    choices = ((1, 'Win'), (-1, 'Lose'), (0, 'None'))

    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True)
    player = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, null=True, blank=True)
    deck = models.ForeignKey(DeckThema, on_delete=models.PROTECT)
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT)
    result1 = models.IntegerField(choices=choices)
    result2 = models.IntegerField(choices=choices)
    result3 = models.IntegerField(choices=choices)
    point = models.IntegerField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.match.date.strftime('%m/%d %H:%M') + "\t" + str(self.player)

class UseDeck(models.Model):
    """使用デッキ"""
    player = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, null=True, blank=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True)
    image1 = models.ImageField(upload_to='decks')
    image2 = models.ImageField(upload_to='decks', blank=True, null=True)
    submit_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.match)

class MatchRecord(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player1 = models.JSONField()
    player2 = models.JSONField()

    def __str__(self):
        return str(self.match)

class DeckRecord(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    thema1 = models.ForeignKey(DeckThema, on_delete=models.PROTECT, related_name='thema1')
    thema2 = models.ForeignKey(DeckThema, on_delete=models.PROTECT, related_name='thema2')
    score1 = models.IntegerField()
    score2 = models.IntegerField()

    def __str__(self):
        return str(self.match)

class UserImage(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_image', default='user_image/kaizoku_man.png')

    def __str__(self):
        return self.user.username

class Point(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    win = models.IntegerField()
    lose = models.IntegerField()
    point = models.IntegerField()

    def __str__(self):
        return self.user.username
