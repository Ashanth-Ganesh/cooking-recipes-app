import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { FavoriteRecipe, Recipe } from '../models/recipe.model';

@Injectable({ providedIn: 'root' })
export class FavoritesService {
  private readonly API = 'http://localhost:8000/api/favorites';
  private favSubject = new BehaviorSubject<FavoriteRecipe[]>([]);
  favorites$ = this.favSubject.asObservable();

  constructor(private http: HttpClient) {}

  load(): Observable<FavoriteRecipe[]> {
    return this.http.get<FavoriteRecipe[]>(this.API).pipe(
      tap((favs) => this.favSubject.next(favs))
    );
  }

  save(recipe: Recipe): Observable<any> {
    return this.http
      .post(this.API, {
        spoonacular_id: recipe.id,
        recipe_name: recipe.title,
        image_url: recipe.image,
        ready_in_minutes: recipe.readyInMinutes,
        servings: recipe.servings,
        recipe_type: recipe.dishTypes?.[0] ?? '',
        recipe_cuisine: recipe.cuisines?.[0] ?? '',
      })
      .pipe(tap(() => this.load().subscribe()));
  }

  remove(recipeId: number): Observable<any> {
    return this.http
      .delete(`${this.API}/${recipeId}`)
      .pipe(tap(() => this.load().subscribe()));
  }

  addCustom(recipe: any): Observable<any> {
    return this.http.post(`${this.API}/custom`, recipe);
  }

  isSaved(spoonacularId: number): boolean {
    return this.favSubject.value.some((f) => f.spoonacular_id === spoonacularId);
  }

  getFavoriteRecipeId(spoonacularId: number): number | null {
    const fav = this.favSubject.value.find((f) => f.spoonacular_id === spoonacularId);
    return fav ? fav.recipe_id : null;
  }
}
