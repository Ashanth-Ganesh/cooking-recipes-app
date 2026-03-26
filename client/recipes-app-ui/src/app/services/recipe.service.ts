import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Recipe, SearchResult } from '../models/recipe.model';

export interface SearchParams {
  query?: string;
  cuisine?: string;
  diet?: string;
  intolerances?: string;
  meal_type?: string;
  max_ready_time?: number | null;
  ingredients?: string;
  number?: number;
  offset?: number;
}

@Injectable({ providedIn: 'root' })
export class RecipeService {
  private readonly API = 'http://localhost:8000/api/recipes';

  constructor(private http: HttpClient) {}

  search(params: SearchParams): Observable<SearchResult> {
    let p = new HttpParams();
    if (params.query) p = p.set('query', params.query);
    if (params.cuisine) p = p.set('cuisine', params.cuisine);
    if (params.diet) p = p.set('diet', params.diet);
    if (params.intolerances) p = p.set('intolerances', params.intolerances);
    if (params.meal_type) p = p.set('meal_type', params.meal_type);
    if (params.max_ready_time) p = p.set('max_ready_time', String(params.max_ready_time));
    if (params.ingredients) p = p.set('ingredients', params.ingredients);
    if (params.number) p = p.set('number', String(params.number));
    if (params.offset !== undefined) p = p.set('offset', String(params.offset));
    return this.http.get<SearchResult>(`${this.API}/search`, { params: p });
  }

  getById(id: number): Observable<Recipe> {
    return this.http.get<Recipe>(`${this.API}/${id}`);
  }

  searchByIngredients(ingredients: string, number = 12): Observable<any[]> {
    const p = new HttpParams().set('ingredients', ingredients).set('number', String(number));
    return this.http.get<any[]>(`${this.API}/by-ingredients`, { params: p });
  }
}
