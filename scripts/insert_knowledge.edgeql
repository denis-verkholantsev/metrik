insert Knowledge {
    name := <str>$name,
    content := <str>$content,
    author := (select User filter .id = <uuid>$user_uid),
    skill := (select Skill filter .id = <uuid>$skill_uid)
};
