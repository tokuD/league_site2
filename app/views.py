from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from .models import DeckThema, Match, Skill, Result, UseDeck, MatchRecord, DeckRecord, UserImage, Point
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import UseDeckForm, MatchForm, ResultForm, SearchForm
from django.contrib import messages
from django.db.models import Q
import json
from django.db.models import Sum
from django.core.paginator import Paginator

def make_choice():
    choices = []
    users = get_user_model().objects.all()
    for user in users:
        choices.append((user, user))
    return choices

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            input_username = form.cleaned_data['username']
            input_password = form.cleaned_data['password1']
            new_user = authenticate(
                username=input_username,
                password=input_password,
            )
            if new_user is not None:
                login(request, new_user)
                return redirect('app:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'app/signup.html', {'form': form})


def index(request):
    return render(request, 'app/index.html')

"""ユーザー一覧"""
def user_index(request, num=1):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            player = form.cleaned_data['player']
            users = get_user_model().objects.filter(username__icontains=player)
            user_images = UserImage.objects.filter(user=users).order_by('-user')
            pages = Paginator(user_images, 12)
            page = pages.get_page(num)
        return render(request, 'app/user_index.html', {'user_images': user_images, 'form': form})
    else:
        form = SearchForm()
        users = get_user_model().objects.all()
        for user in users:
            try:
                image = UserImage.objects.get(user=user)
            except UserImage.DoesNotExist:
                UserImage.objects.create(user=user)
            user_images = UserImage.objects.all().order_by('-user')
            pages = Paginator(user_images, 12)
            page = pages.get_page(num)
        return render(request, 'app/user_index.html', {'user_images': page, 'form': form})

"""ユーザー詳細"""
def user_detail(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    matches = Match.objects.filter(Q(player1=user) | Q(player2=user)).order_by('-date')
    decks = UseDeck.objects.filter(player=user).order_by('-submit_time')
    return render(request, 'app/user_detail.html', {'user': user, 'matches': matches, 'decks': decks})

"""試合一覧"""
def match_index(request, num=1):
    matches = Match.objects.all().order_by('-date')
    pages = Paginator(matches, 10)
    page = pages.get_page(num)
    return render(request, 'app/match_index.html', {'matches': page})

"""デッキ画像取得"""
def get_deck(deckname):
    deck = DeckThema.objects.get(name=deckname)
    return deck

"""試合結果"""
def match_detail(request, pk):
    match = get_object_or_404(Match, pk=pk)
    try:
        record = MatchRecord.objects.get(match=match)
        if record.player1 != {} and record.player2 != {}:
            results = {
                'match': record.match,
                'player1': record.player1["player"],
                'deck1': get_deck(record.player1["deck"]),
                'skill1': record.player1["skill"],
                'result11': record.player1["result1"],
                'result12': record.player1["result2"],
                'result13': record.player1["result3"],
                'point11': record.player1["point"],
                'score1': record.player1["score"],
                'comment1': record.player1["comment"],
                'player2': record.player2["player"],
                'deck2': get_deck(record.player2["deck"]),
                'skill2': record.player2["skill"],
                'result21': record.player2["result1"],
                'result22': record.player2["result2"],
                'result23': record.player2["result3"],
                'point2': record.player2["point"],
                'score2': record.player2["score"],
                'comment2': record.player2["comment"],
            }
            return render(request, 'app/match_detail.html', results)
        elif record.player1 != {}:
                results = {
                    'match': record.match,
                    'player1': record.player1["player"],
                    'deck1': get_deck(record.player1["deck"]),
                    'skill1': record.player1["skill"],
                    'result11': record.player1["result1"],
                    'result12': record.player1["result2"],
                    'result13': record.player1["result3"],
                    'point11': record.player1["point"],
                    'score1': record.player1["score"],
                    'comment1': record.player1["comment"],
                }
                return render(request, 'app/match_detail.html', results)
        elif record.player2 != {}:
                results = {
                    'match': record.match,
                    'player2': record.player2["player"],
                    'deck2': get_deck(record.player2["deck"]),
                    'skill2': record.player2["skill"],
                    'result21': record.player2["result1"],
                    'result22': record.player2["result2"],
                    'result23': record.player2["result3"],
                    'point22': record.player2["point"],
                    'score2': record.player2["score"],
                    'comment2': record.player2["comment"],
                }
                return render(request, 'app/match_detail.html', results)
    except MatchRecord.DoesNotExist:
        if request.user in [match.player1, match.player2]:
            messages.success(request, '結果を入力してください')
            return redirect('app:submit_result', pk=match.pk)
        else:
            messages.success(request, '入力待ちです')
            return redirect('app:match_index')



"""結果入力関数"""
def fill_record(match):
    records = Result.objects.filter(match=match)
    player1 = {}
    player2 = {}
    players = [player1, player2]
    i = 0
    for record in records:
        players[i] = {
                "player": records[i].player.username,
                "deck": records[i].deck.name,
                "skill": records[i].skill.skill_name,
                "result1": records[i].result1,
                "result2": records[i].result2,
                "result3": records[i].result3,
                "point": records[i].point,
                "score": records[i].score,
                "comment": records[i].comment,
        }
        json.dumps(players[i])
        i += 1
    try:
        record = MatchRecord.objects.get(match=match)
        record.player1 = players[0]
        record.player2 = players[1]
        record.save()
        return
    except MatchRecord.DoesNotExist:
        record = MatchRecord(match=match, player1=players[0], player2=players[1])
        record.save()
    return


"""試合結果報告"""
@login_required
def submit_result(request, pk):
    message = '編集しました'
    match = get_object_or_404(Match, pk=pk)
    try:
        instance = Result.objects.get(player=request.user, match=match)
        if request.method == 'POST':
            form = ResultForm(request.POST, instance=instance)
            if form.is_valid():
                form = form.save(commit=False)
                form.player = request.user
                form.match = match
                form.point = form.result1 + form.result2 + form.result3
                results = [form.result1, form.result2, form.result3]
                form.score = 0
                for result in results:
                    if result == 1:
                        form.score += 1
                form.save()
                fill_record(match)
                messages.success(request, message)
            return redirect('app:match_detail', pk=match.pk)
        else:
            form = ResultForm(instance=instance)
        return render(request, 'app/submit_result.html', {'match': match, 'form': form})
    except Result.DoesNotExist:
        if request.method == 'POST':
            form = ResultForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.player = request.user
                form.match = match
                form.point = form.result1 + form.result2 + form.result3
                results = [form.result1, form.result2, form.result3]
                form.score = 0
                for result in results:
                    if result == 1:
                        form.score += 1
                form.save()
                fill_record(match)
                messages.success(request, message)
            return redirect('app:match_detail', pk=match.pk)
        else:
            form = ResultForm()
        return render(request, 'app/submit_result.html', {'match': match, 'form': form})



"""デッキ提出フォーム"""
@login_required
def submit_deck(request, pk):
    message = '提出が完了しました'
    match = get_object_or_404(Match, pk=pk)
    try:
        instance = UseDeck.objects.get(player=request.user, match=match)
        if request.method == 'POST':
            form = UseDeckForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                deck = form.save(commit=False)
                deck.match = match
                deck.save()
                messages.success(request, message)
            return redirect('app:user_detail', pk=request.user.pk)
        else:
            form = UseDeckForm(instance=instance)
        return render(request, 'app/submit_deck.html', {'form': form, 'match': match})
    except UseDeck.DoesNotExist:
        if request.method == 'POST':
            form = UseDeckForm(request.POST, request.FILES)
            if form.is_valid():
                deck = form.save(commit=False)
                deck.player = request.user
                deck.match = match
                deck.save()
                messages.success(request, message)
            return redirect('app:user_detail', pk=request.user.pk)
        else:
            form = UseDeckForm()
        return render(request, 'app/submit_deck.html', {'form': form, 'match': match})



"""試合登録"""
@login_required
def register_match(request):
    message = "登録が完了しました"
    form = MatchForm(request.POST or None)
    choices = make_choice()
    form.fields["player2"].choices = choices
    if form.is_valid():
        match = Match()
        match.player1 = request.user
        player2 = form.cleaned_data['player2']
        match.player2 = get_user_model().objects.get(username=player2)
        match.date = form.cleaned_data['date']
        Match.objects.create(
            player1=match.player1,
            player2=match.player2,
            date=match.date,
        )
        return redirect('app:match_index', page_num=1)
    return render(request, 'app/register_match.html', {'form': form})


"""試合編集"""
@login_required
def edit_match(request, pk):
    message = "編集しました"
    match = get_object_or_404(Match, pk=pk)
    if request.method == 'POST':
        form = MatchForm(request.POST)
        choices = make_choice()
        form.fields["player2"].choices = choices
        if form.is_valid():
            match.player1 = request.user
            player2 = form.cleaned_data["player2"]
            match.player2 = get_user_model().objects.get(username=player2)
            match.date = form.cleaned_data["date"]
            match.save()
        return redirect('app:match_index')
    else:
        initial = dict(
            player1=request.user,
            player2=match.player2,
            date=match.date.strftime('%Y-%m-%dT%H:%M')
        )
        form = MatchForm(initial=initial)
        choices = make_choice()
        form.fields["player2"].choices = choices
        form.player2 = get_user_model().objects.get(username=match.player2)
    return render(request, 'app/edit_match.html', {'form': form, 'match': match})



"""試合削除"""
@require_POST
def delete_match(request, pk):
    message = '削除しました'
    if request.method == 'POST':
        match = get_object_or_404(Match, pk=pk)
        match.delete()
        messages.success(request, message)
    return redirect('app:match_index', page_num=1)


"""デッキテーマ一覧"""
def deckthema_index(request):
    decks = DeckThema.objects.all().order_by('-tier')
    return render(request, 'app/deckthema_index.html', {'decks': decks})


"""デッキテーマ詳細"""
def deckthema_detail(request, pk):
    deck = get_object_or_404(DeckThema, pk=pk)
    return render(request, 'app/deckthema_detail.html', {'deck': deck})


"""相性表作成"""
def make_table(match):
    match_record = MatchRecord.objects.get(match=match)
    if match_record.player1 != {} and match_record.player2 != {}:
        player1 = match_record.player1
        player2 = match_record.player2
        thema1 = DeckThema.objects.get(name=player1["deck"])
        thema2 = DeckThema.objects.get(name=player2["deck"])
        score1 = match_record.player1["score"]
        score2 = match_record.player2["score"]
        try:
            deck_record = DeckRecord.objects.get(match=match)
            deck_record.thema1 = thema1
            deck_record.thema2 = thema2
            deck_record.score1 = score1
            deck_record.score2 = score2
            return
        except DeckRecord.DoesNotExist:
            deck_record = DeckRecord.objects.create(
                match=match,
                thema1 = thema1,
                thema2 = thema2,
                score1 = score1,
                score2 = score2
            )
            return

"""DeckRecordから対面勝ち数を計算"""
def calc_win(thema1, thema2):
    records = DeckRecord.objects.filter(thema1=thema1, thema2=thema2)
    win = 0
    for record in records:
        win += record.score1
    records = DeckRecord.objects.filter(thema1=thema2, thema2=thema1)
    for record in records:
        win += record.score2
    return win

"""相性表"""
def deck_records(request):
    match_records = MatchRecord.objects.all()
    for match_record in match_records:
        make_table(match_record.match)
    decks = DeckThema.objects.all().order_by('-tier')[0:10]
    win_lose = []
    rates = []
    for row in decks:
        row1 = []
        row2 = []
        for colum in decks:
            win = calc_win(row, colum)
            lose = calc_win(colum, row)
            try:
                rate = round(win * 100 / (win + lose), 1)
            except ZeroDivisionError:
                rate = "No Data"
            row1.append(str(win) + "-" + str(lose))
            row2.append(rate)
        win_lose.append(row1)
        rates.append(row2)
    return render(request, 'app/deck_records.html', {'win_lose': win_lose, 'decks': decks, 'rates': rates})

"""得点計算"""
def calc_point(user):
    win = 0
    lose = 0
    point = 0
    results = Result.objects.filter(player=user)
    for result in results:
        if result.score >= 2:
            win += 1
        else:
            lose += 1
        point += result.point
    return {'win': win, 'lose': lose, 'point': point}


"""順位表"""
def rank(request):
    users = get_user_model().objects.all()
    for user in users:
        params = calc_point(user)
        try:
            point = Point.objects.get(user=user)
            point.win = params["win"]
            point.lose = params["lose"]
            point.point = params["point"]
            point.save()
        except Point.DoesNotExist:
            point = Point.objects.create(
                user=user,
                win = params["win"],
                lose = params["lose"],
                point = params["point"],
            )
            point.save()
    records = Point.objects.all().order_by('-win', 'lose', '-point')
    return render(request, 'app/rank.html', {'records': records})
