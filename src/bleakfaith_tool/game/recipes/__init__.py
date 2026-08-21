from bleakfaith_tool.game import Game

from .recipe import Recipe as Recipe


def recipes_from_game(game: Game) -> list[Recipe]:
    recipe_dt = game.data_table("DT_Recipes")
    return [Recipe(k, v, game) for k, v in recipe_dt.rows.items()]
