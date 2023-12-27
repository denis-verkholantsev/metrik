update SkillTree
filter .id = <uuid>$uid and .author.id = <uuid>$author
set {
    name := <str>$name,
    description := <optional str>$description
};
