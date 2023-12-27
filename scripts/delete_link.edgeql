with
tree:= (select SkillTree filter .id=<uuid>$tree and .author.id=<uuid>$author),
update Skill filter .id=<uuid>$source and .tree.id=tree.id
set{
    contains -= (select detached Skill filter .id=<uuid>$target)
};
