from django.urls import path, include
from component import views

urlpatterns = [
  path('latest-components', views.LastUpdatedComponentsList.as_view()),
  path('components', views.AllComponents.as_view()),
  path('component', views.AddComponent.as_view()),
  path('categories', views.CategoriesList.as_view()),
  path('category/<slug:category_slug>', views.CategoryDetail.as_view()),
  path('component/<int:component_id>', views.ComponentDetail.as_view()),
  path('delete-component/<int:component_id>', views.DeleteComponent.as_view()),
  path('components/<slug:category_slug>', views.ComponentsOfCategory.as_view()), #TODO: use query param with question mark
  path('compartments', views.CompartmentsList.as_view()),
  path('compartment/<int:compartment_id>', views.CompartmentDetail().as_view()),
  path('components/compartment=<int:compartment_id>', views.ComponentsInCompartment.as_view()),
  path('components/search/', views.searchComponent),
  path('register', views.RegisterView.as_view(), name='auth_register')
]