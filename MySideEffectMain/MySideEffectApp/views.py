from django.shortcuts import render

from .forms import SignUp, UserForm, Search
from .models import Occurence

from bokeh.charts import Bar, defaults
from bokeh.resources import CDN
from bokeh.embed import components
from .total_prescriptions import prescription_data

from pandas import DataFrame
from django.conf import settings

from os.path import join as path_join

# Create your views here.


def home(request):
    """
        Index Page with a search bar for drugs.
        Creates a table with all the Adverse Events of a drug,
        how often each occured and other information.
    """
    if request.method == 'POST':
        form = Search(request.POST)
        if form.is_valid():
            form_weight = "50-100"
            form_age = "12-90"

            drug = form.cleaned_data["search_drug"]

            def format_age_weight(form_info):
                if "-" in form_info:
                    return tuple(map(int, form_info.split("-")))
                else:
                    if form_info.startswith("under"):
                        return 0, int(form_info.lstrip("under"))
                    elif form_info.startswith("over"):
                        return int(form_info.lstrip("over")), 1000
                    else:
                        raise ValueError("Invalid input specified!")

            lower_age, upper_age = format_age_weight(form_age)
            lower_weight, upper_weight = format_age_weight(form_weight)

            form_gender = "Male"
            form_location = "Europa"

            res_list = Occurence.objects.filter(continent=form_location).filter(gender=form_gender).filter(age__lte=upper_age).filter(age__gte=lower_age).filter(weight__lte=upper_weight).filter(weight__gte=lower_weight).filter(drug_names__icontains=drug)

            attribute_list = [
                "adverse_effects", "drug_names", "age", "weight", "gender",
                "continent", "literature_reference",
            ]

            import json
            adverse_effects = []

            for el in res_list:
                for effect in json.loads(getattr(el, "adverse_effects")):
                    adverse_effects.append(effect)
            from collections import Counter
            adverse_effects_count = Counter(adverse_effects)

            effects, counts = [], []

            pd = prescription_data(
                path_join(settings.BASE_DIR, "prescription_population.csv"),
                path_join(settings.BASE_DIR, "total_medicine_prescriptions.csv")
            )
            # XXX COMPUTE CHARACTERISTIC FROM CONTINENT AND GENDER
            n_prescriptions_per_year= pd.compute_data(
                characteristic=form_gender,
                medicine=drug
            )

            n_prescriptions = n_prescriptions_per_year / 23.

            for effect, count in adverse_effects_count.most_common():
                effects.append(effect)
                counts.append(float(count) / n_prescriptions)

            try:
                defaults.width = 1000
                defaults.height = 1000

                df = DataFrame(list(adverse_effects_count.items()), columns=['Drug', 'Occurence'])
                plot = Bar(df, label="Drug", values="Occurence")

                script, div = components(plot, CDN)
            except ValueError:
                plot = False
            else:
                plot = True


            if plot:
                return render(request, 'MySideEffectApp/result.html', {
                    'res_list': adverse_effects_count.most_common(),
                    'attribute_list': ["adverse_effects", "counts"],
                    'the_script': script,
                    "the_div": div,
                    'drug_name': drug,
                })

            else:
                return render(request, 'MySideEffectApp/result.html', {
                    'res_list': adverse_effects_count.most_common(),
                    'attribute_list': ["adverse_effects", "counts"],
                    'drug_name': drug,
                })

    personal_info_form = Search()
    return render(request, 'MySideEffectApp/home.html', {
        'personal_info_form': personal_info_form,
    })


def about(request):
    return render(request, 'MySideEffectApp/about.html')


def contact(request):
    return render(request, 'MySideEffectApp/contact.html')


def sponsors(request):
    return render(request, 'MySideEffectApp/sponsors.html')


def result(request):
    return render(request, 'MySideEffectApp/result.html')


def preferences(request):
    """
        Your preferences page to change the information about the user set at
        signing up (i.e. new drug the user takes).
    """
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form_weight = form.cleaned_data["weight"]
            form_age = form.cleaned_data["age"]

            def format_age_weight(form_info):
                if "-" in form_info:
                    return tuple(map(int, form_info.split("-")))
                else:
                    if form_info.startswith("under"):
                        return 0, int(form_info.lstrip("under"))
                    elif form_info.startswith("over"):
                        return int(form_info.lstrip("over")), 1000
                    else:
                        raise ValueError("Invalid input specified!")

            lower_age, upper_age = format_age_weight(form_age)
            lower_weight, upper_weight = format_age_weight(form_weight)

            form_gender = form.cleaned_data["gender"]
            form_location = form.cleaned_data["location"]
            print(form_gender)
            res_list = Occurence.objects.filter(continent=form_location).filter(gender=form_gender).filter(age__lte=upper_age).filter(age__gte=lower_age).filter(weight__lte=upper_weight).filter(weight__gte=lower_weight)

            attribute_list = [
                "adverse_effects", "drug_names", "age", "weight", "gender",
                "continent", "literature_reference",
            ]
            res_list = [tuple(map(lambda x: getattr(el, x), attribute_list)) for el in res_list]
            return render(request, 'MySideEffectApp/saved_prefs.html', {
                'res_list': res_list,
                'attribute_list': attribute_list,
            })

    personal_info_form = UserForm()
    return render(request, 'MySideEffectApp/preferences.html', {
        'personal_info_form': personal_info_form,
    })


def register(request):
    """
        The register page to set your username, password, e-mail and personal
        information.
    """
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            form_weight = form.cleaned_data["weight"]
            form_age = form.cleaned_data["age"]

            def format_age_weight(form_info):
                if "-" in form_info:
                    return tuple(map(int, form_info.split("-")))
                else:
                    if form_info.startswith("under"):
                        return 0, int(form_info.lstrip("under"))
                    elif form_info.startswith("over"):
                        return int(form_info.lstrip("over")), 1000
                    else:
                        raise ValueError("Invalid input specified!")

            lower_age, upper_age = format_age_weight(form_age)
            lower_weight, upper_weight = format_age_weight(form_weight)

            form_gender = form.cleaned_data["gender"]
            form_location = form.cleaned_data["location"]

            res_list = Occurence.objects.filter(continent=form_location).filter(gender=form_gender).filter(age__lte=upper_age).filter(age__gte=lower_age).filter(weight__lte=upper_weight).filter(weight__gte=lower_weight)

            attribute_list = [
                "adverse_effects", "drug_names", "age", "weight", "gender",
                "continent", "literature_reference",
            ]
            res_list = [tuple(map(lambda x: getattr(el, x), attribute_list)) for el in res_list]
            return render(request, 'MySideEffectApp/result.html', {
                'res_list': res_list,
                'attribute_list': attribute_list,
            })

    personal_info_form = SignUp()
    return render(request, 'MySideEffectApp/home.html', {
        'personal_info_form': personal_info_form,
    })
