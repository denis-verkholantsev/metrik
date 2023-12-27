 select Skill {*, author} filter .tree.id=<uuid>$tree and (.tree.public=true or .tree.author.id=<uuid>$user);
