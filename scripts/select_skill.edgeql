select Skill { *, tree, author }
filter .id = <uuid>$skill_uid
and .tree.author.id = <uuid>$author_uid;
