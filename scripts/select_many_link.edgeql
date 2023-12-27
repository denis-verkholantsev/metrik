select Skill {id, contains}
filter .tree.id = <uuid>$tree
and .tree.author.id = <uuid>$author;
