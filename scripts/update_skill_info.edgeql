update Skill
filter .id = <uuid>$skill and .tree.author.id=<uuid>$author
set{
    name:=<str>$name,
    description:=<optional str>$description,
    x:=<float64>$x,
    y:=<float64>$y
};
