import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';
import { HomeComponent } from './components/home/home.component';
import { RecipeSearchComponent } from './components/recipe-search/recipe-search.component';
import { RecipeDetailComponent } from './components/recipe-detail/recipe-detail.component';
import { LoginComponent } from './components/login/login.component';
import { SignupComponent } from './components/signup/signup.component';
import { FavoritesComponent } from './components/favorites/favorites.component';
import { ChefUploadComponent } from './components/chef-upload/chef-upload.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'recipes', component: RecipeSearchComponent },
  { path: 'recipes/:id', component: RecipeDetailComponent },
  { path: 'login', component: LoginComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'favorites', component: FavoritesComponent, canActivate: [authGuard] },
  { path: 'chef/upload', component: ChefUploadComponent, canActivate: [authGuard] },
  { path: '**', redirectTo: '' },
];
