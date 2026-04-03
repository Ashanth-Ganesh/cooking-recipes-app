import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { HttpTestingController } from '@angular/common/http/testing';
import { FavoritesService } from './favorites.service';
import { FavoriteRecipe, Recipe } from '../models/recipe.model';

const mockFavorite: FavoriteRecipe = {
  recipe_id: 10,
  spoonacular_id: 42,
  recipe_name: 'Spaghetti Bolognese',
  image_url: 'https://example.com/pasta.jpg',
  ready_in_minutes: 45,
  servings: 4,
  is_custom: false,
  recipe_type: 'main course',
  recipe_cuisine: 'Italian',
};

const mockRecipe: Recipe = {
  id: 42,
  title: 'Spaghetti Bolognese',
  image: 'https://example.com/pasta.jpg',
  readyInMinutes: 45,
  servings: 4,
  cuisines: ['Italian'],
  dishTypes: ['main course'],
};

describe('FavoritesService', () => {
  let service: FavoritesService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [FavoritesService, provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(FavoritesService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('isSaved', () => {
    it('returns false when favorites list is empty', () => {
      expect(service.isSaved(42)).toBe(false);
    });

    it('returns true after a recipe is loaded into favorites', () => {
      service.load().subscribe();
      const req = httpMock.expectOne('http://localhost:8000/api/favorites');
      req.flush([mockFavorite]);
      expect(service.isSaved(42)).toBe(true);
    });

    it('returns false for a recipe not in favorites', () => {
      service.load().subscribe();
      const req = httpMock.expectOne('http://localhost:8000/api/favorites');
      req.flush([mockFavorite]);
      expect(service.isSaved(999)).toBe(false);
    });
  });

  describe('getFavoriteRecipeId', () => {
    it('returns null when favorites list is empty', () => {
      expect(service.getFavoriteRecipeId(42)).toBeNull();
    });

    it('returns the recipe_id for a saved recipe', () => {
      service.load().subscribe();
      const req = httpMock.expectOne('http://localhost:8000/api/favorites');
      req.flush([mockFavorite]);
      expect(service.getFavoriteRecipeId(42)).toBe(10);
    });

    it('returns null for an unsaved recipe', () => {
      service.load().subscribe();
      const req = httpMock.expectOne('http://localhost:8000/api/favorites');
      req.flush([mockFavorite]);
      expect(service.getFavoriteRecipeId(999)).toBeNull();
    });
  });

  describe('load', () => {
    it('GETs the favorites endpoint', () => {
      service.load().subscribe();
      const req = httpMock.expectOne('http://localhost:8000/api/favorites');
      expect(req.request.method).toBe('GET');
      req.flush([mockFavorite]);
    });

    it('updates favorites$ observable with loaded favorites', () => {
      let emitted: FavoriteRecipe[] | undefined;
      service.favorites$.subscribe((f) => (emitted = f));

      service.load().subscribe();
      const req = httpMock.expectOne('http://localhost:8000/api/favorites');
      req.flush([mockFavorite]);

      expect(emitted).toEqual([mockFavorite]);
    });

    it('returns the favorites array', () => {
      let result: FavoriteRecipe[] | undefined;
      service.load().subscribe((f) => (result = f));
      const req = httpMock.expectOne('http://localhost:8000/api/favorites');
      req.flush([mockFavorite]);
      expect(result).toEqual([mockFavorite]);
    });
  });

  describe('save', () => {
    it('POSTs to the favorites endpoint with correct body', () => {
      service.save(mockRecipe).subscribe();

      const saveReq = httpMock.expectOne('http://localhost:8000/api/favorites');
      expect(saveReq.request.method).toBe('POST');
      expect(saveReq.request.body).toEqual({
        spoonacular_id: 42,
        recipe_name: 'Spaghetti Bolognese',
        image_url: 'https://example.com/pasta.jpg',
        ready_in_minutes: 45,
        servings: 4,
        recipe_type: 'main course',
        recipe_cuisine: 'Italian',
      });
      saveReq.flush({ message: 'saved', recipe_id: 10 });

      // save() triggers a load() via tap
      const loadReq = httpMock.expectOne('http://localhost:8000/api/favorites');
      loadReq.flush([mockFavorite]);
    });
  });

  describe('remove', () => {
    it('DELETEs the correct favorites endpoint', () => {
      service.remove(10).subscribe();

      const deleteReq = httpMock.expectOne('http://localhost:8000/api/favorites/10');
      expect(deleteReq.request.method).toBe('DELETE');
      deleteReq.flush({ message: 'removed' });

      // remove() triggers a load() via tap
      const loadReq = httpMock.expectOne('http://localhost:8000/api/favorites');
      loadReq.flush([]);
    });
  });

  describe('addCustom', () => {
    it('POSTs to the custom favorites endpoint', () => {
      const customRecipe = { recipe_name: 'My Recipe', recipe_instructions: 'Cook it.' };
      service.addCustom(customRecipe).subscribe();

      const req = httpMock.expectOne('http://localhost:8000/api/favorites/custom');
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual(customRecipe);
      req.flush({ message: 'added', recipe_id: 99 });
    });
  });
});
