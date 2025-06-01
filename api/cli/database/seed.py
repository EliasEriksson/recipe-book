from api import schemas
from api.database import Database


async def seed_database() -> None:
    async with Database() as client:
        # Languages
        english = await client.languages.create(
            schemas.language.LanguageCreatable("en")
        )

        # Units
        gram = await client.units.create(
            schemas.unit.UnitCreatable(english.language.id, "Gram", "g")
        )
        hectogram = await client.units.create(
            schemas.unit.UnitCreatable(english.language.id, "Hectogram", "hg")
        )
        kilo = await client.units.create(
            schemas.unit.UnitCreatable(english.language.id, "Kilograms", "kg")
        )
        liter = await client.units.create(
            schemas.unit.UnitCreatable(english.language.id, "Liter", "l")
        )
        deciliter = await client.units.create(
            schemas.unit.UnitCreatable(english.language.id, "Deciliter", "dl")
        )
        centiliter = await client.units.create(
            schemas.unit.UnitCreatable(english.language.id, "Centiliter", "cl")
        )
        milliliter = await client.units.create(
            schemas.unit.UnitCreatable(english.language.id, "Milliliter", "ml")
        )

        # Ingredients
        sugar = await client.ingredients.create(
            schemas.ingredient.IngredientCreatable(english.language.id, "Sugar")
        )
        water = await client.ingredients.create(
            schemas.ingredient.IngredientCreatable(english.language.id, "Water")
        )
        lime_juice = await client.ingredients.create(
            schemas.ingredient.IngredientCreatable(english.language.id, "Lime juice")
        )
        light_rum = await client.ingredients.create(
            schemas.ingredient.IngredientCreatable(english.language.id, "Light rum")
        )
        ice = await client.ingredients.create(
            schemas.ingredient.IngredientCreatable(english.language.id, "Ice")
        )
        simple_syrup_ingredient = await client.ingredients.create(
            schemas.ingredient.IngredientCreatable(english.language.id, "Simple syrup")
        )

        # Recipes
        simple_syrup_recipe = await client.recipes.create(
            schemas.recipe.RecipeCreatable(english.language.id, "Simple syrup")
        )
        await client.recipe_ingredients.create(
            schemas.recipe_ingredient.RecipeIngredientCreatable(
                simple_syrup_recipe.recipe.id,
                sugar.ingredient.id,
                english.language.id,
                deciliter.unit.id,
                3,
                "",
                "",
            )
        )
        await client.recipe_ingredients.create(
            schemas.recipe_ingredient.RecipeIngredientCreatable(
                simple_syrup_recipe.recipe.id,
                water.ingredient.id,
                english.language.id,
                deciliter.unit.id,
                3,
                "",
                "",
            )
        )

        daiquiri = await client.recipes.create(
            schemas.recipe.RecipeCreatable(english.language.id, "Daiquiri")
        )
        await client.recipe_ingredients.create(
            schemas.recipe_ingredient.RecipeIngredientCreatable(
                daiquiri.recipe.id,
                light_rum.ingredient.id,
                english.language.id,
                centiliter.unit.id,
                5,
                "",
                "Havana Club",
            )
        )
        await client.recipe_ingredients.create(
            schemas.recipe_ingredient.RecipeIngredientCreatable(
                daiquiri.recipe.id,
                lime_juice.ingredient.id,
                english.language.id,
                centiliter.unit.id,
                3,
                "",
                "",
            )
        )
        await client.recipe_ingredients.create(
            schemas.recipe_ingredient.RecipeIngredientCreatable(
                daiquiri.recipe.id,
                simple_syrup_ingredient.ingredient.id,
                english.language.id,
                centiliter.unit.id,
                2,
                "",
                "",
            )
        )
        await client.recipe_ingredients.create(
            schemas.recipe_ingredient.RecipeIngredientCreatable(
                daiquiri.recipe.id,
                ice.ingredient.id,
                english.language.id,
                deciliter.unit.id,
                1,
                "",
                "",
            )
        )
