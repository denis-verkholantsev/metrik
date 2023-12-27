with
    selected_tree:=(select SkillTree{*} filter .id = <uuid>$tree and .author.id=<uuid>$author),
    new_skill:=(for _ in selected_tree union (
    insert Skill{
        name:=<str>$name,
        description:=<optional str>$description,
        author:=(select User filter .id=<uuid>$author),
        tree:=selected_tree,
        x:=<float64>$x,
        y:=<float64>$y,
        })),
select {new_skill};
