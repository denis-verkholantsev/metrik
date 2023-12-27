update Knowledge
filter .id = <uuid>$knowledge_uid and .author.id=<uuid>$author_uid
set{
    name:=<str>$name,
    content:=<str>$content,
};
