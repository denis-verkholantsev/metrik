insert SkillTree {
    name := <str>$name,
    description := <optional str>$description,
    public := <bool>$public,
    public_grades := <bool>$public_grades,
    author := (select User filter .id = <uuid>$author),
};
