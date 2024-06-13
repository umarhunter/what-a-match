from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.forms import formset_factory
from matching.games import StableMarriage, StableRoommates
from .forms import InputForm, IntegerInputForm, PrefsInputForm


class StorageContainer:
    dictionary = {}
    suitor_list = []
    reviewer_list = []

    def clear(self):
        self.suitor_list.clear()
        self.reviewer_list.clear()
        # self.dictionary.clear()


# views here.
def stable_marriage(request):
    """The Stable Marriage (Gale & Shapley) page"""

    # initialization for demo
    suitor_prefs = {
        'David': ['Emily', 'Olivia', 'Sophie', 'Eleanor'],
        'Daniel': ['Sophie', 'Olivia', 'Emily', 'Eleanor'],
        'Andrew': ['Eleanor', 'Sophie', 'Olivia', 'Emily'],
        'Ryan': ['Emily', 'Olivia', 'Sophie', 'Eleanor']
    }

    reviewer_prefs = {
        'Emily': ['David', 'Ryan', 'Daniel', 'Andrew'],
        'Olivia': ['Daniel', 'Andrew', 'David', 'Ryan'],
        'Sophie': ['David', 'Daniel', 'Andrew', 'Ryan'],
        'Eleanor': ['Andrew', 'Ryan', 'Daniel', 'David']
    }

    # set-up dictionaries with player information's before solving
    game = StableMarriage.create_from_dictionaries(
        suitor_prefs, reviewer_prefs
    )
    results = game.solve()

    # POST data submitted; we may now process form inputs
    if request.method == "POST":
        int_form = IntegerInputForm(request.POST)
        num = int_form['number'].value()
        if int_form.is_valid():
            request.session['num'] = num
            return redirect('match:sm_matching_suitors')
    else:
        # no POST data, create a new/blank form
        int_form = IntegerInputForm()  # we need to know the number of individuals

    context = {'results': results,
               'suitor_prefs_dict': suitor_prefs,
               'reviewer_prefs_dict': reviewer_prefs,
               'int_form': int_form}
    return render(request, 'match/stable_marriage.html', context)


def sm_matching_suitors(request):
    """ Retrieve all suitors """

    num = int(request.session.get('num'))
    if not num:
        # Handle the case where 'num' is not set in the session
        return redirect('match:stable_marriage')  # Redirect to a view that sets 'num'

    SuitorFormSet = formset_factory(InputForm, min_num=int(num / 2), validate_min=True, extra=0)

    if request.method == "POST":
        # POST data submitted
        suitors = SuitorFormSet(request.POST, prefix='suitors')

        if suitors.is_valid():
            for suitor in suitors:
                cd = suitor.cleaned_data
                name = cd.get('name')
                StorageContainer.suitor_list.append(name)

            return redirect("match:sm_matching_reviewers")  # Redirect to avoid re-submission
        else:
            print("Formsets are not valid")
    else:
        # no POST data
        suitors = SuitorFormSet(prefix='suitors')

    return render(request, 'match/sm_matching_suitors.html', {
        'suitors': suitors,
    })


def sm_matching_reviewers(request):
    """ Retrieve all reviewers """
    num = int(request.session.get('num'))
    if not num:
        # Handle the case where 'num' is not set in the session
        return redirect('match:stable_marriage')  # Redirect to a view that sets 'num'

    ReviewerFormSet = formset_factory(InputForm, min_num=int(num / 2), validate_min=True, extra=0)

    if request.method == "POST":
        # POST data submitted
        reviewers = ReviewerFormSet(request.POST)

        if reviewers.is_valid():
            for reviewer in reviewers:
                cd = reviewer.cleaned_data
                name = cd.get('name')
                StorageContainer.reviewer_list.append(name)
            return redirect("match:sm_matching_1")  # Redirect to avoid re-submission
        else:
            print("Reviewer formsets are not valid")
    else:
        # no POST data
        reviewers = ReviewerFormSet()

    return render(request, 'match/sm_matching_reviewers.html', {
        'reviewers': reviewers
    })


def sm_matching(request):
    """The Stable Marriage Matching Page"""

    num = int(request.session.get('num'))
    if not num:
        # Handle the case where 'num' is not set in the session
        return redirect('match:stable_marriage')  # Redirect to a view that sets 'num'

    SuitorFormSet = formset_factory(InputForm, min_num=int(num / 2), validate_min=True, extra=0)
    ReviewerFormSet = formset_factory(InputForm, min_num=int(num / 2), validate_min=True, extra=0)

    if request.method == "POST":
        # POST data submitted
        suitors = SuitorFormSet(request.POST, prefix='suitors')
        reviewers = ReviewerFormSet(request.POST, prefix='reviewers')

        if suitors.is_valid():

            return redirect("match:sm_matching_1")  # Redirect to avoid re-submission
        else:
            print("Formsets are not valid")
    else:
        # no POST data
        reviewers = ReviewerFormSet(prefix='reviwers')
        suitors = SuitorFormSet(prefix='suitors')

    return render(request, 'match/sm_matching.html', {
        'suitors': suitors,
        'reviewers': reviewers
    })


def sm_matching_1(request):
    """The Stable Marriage Matching Pt. 2"""

    suitors = StorageContainer.suitor_list
    reviewers = StorageContainer.reviewer_list

    num = len(suitors) + len(reviewers)

    PrefsFormSet = formset_factory(PrefsInputForm, min_num=int(num / 2), validate_min=True, extra=0)

    if request.method == "POST":
        # POST data submitted


        if PrefsFormSet.is_valid():
            # Perform matching logic or save data

            return redirect("match:sm_matching_1")  # Redirect to avoid re-submission
        else:
            print("Formset is not valid")
    else:
        formset = InputForm()
    context = {'suitors': suitors, 'reviewers': reviewers}
    return render(request, 'match/sm_matching_1.html', context)


def sm_matching_complete(request):
    """Displays the results of the SM matching"""

    return render(request, 'match/sm_matching_complete.html', {})


def stable_roommate(request):
    """The Stable Roommate (Robert Irving) page"""

    suitor_with_prefs = {
        'David': ['Emily', 'Olivia', 'Sophie', 'Eleanor'],
        'Daniel': ['Sophie', 'Olivia', 'Emily', 'Eleanor'],
        'Andrew': ['Eleanor', 'Sophie', 'Olivia', 'Emily'],
        'Ryan': ['Emily', 'Olivia', 'Sophie', 'Eleanor'],
        'Emily': ['David', 'Ryan', 'Daniel', 'Andrew'],
        'Olivia': ['Daniel', 'Andrew', 'David', 'Ryan'],
        'Sophie': ['David', 'Daniel', 'Andrew', 'Ryan'],
        'Eleanor': ['Andrew', 'Ryan', 'Daniel', 'David'],
    }

    # Ensure that each player has ranked all other players
    players = set(suitor_with_prefs.keys())
    for player, preferences in suitor_with_prefs.items():
        if set(preferences) != players - {player}:
            missing_players = players - set(preferences) - {player}
            suitor_with_prefs[player].extend(list(missing_players))

    game = StableRoommates.create_from_dictionary(suitor_with_prefs)
    results = game.solve()

    return render(request, 'match/stable_roommate.html', {'results': results,
                                                          'suitor_prefs_dict': suitor_with_prefs})


def boehmer_heeger(request):
    """ Boehmer & Heeger's adapting stable marriage page """
    return render(request, 'match/boehmer_heeger.html')
