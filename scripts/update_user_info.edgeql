update User filter .id = <uuid>$uid
set {
    first_name := <str>$first_name,
    last_name := <str>$last_name,
    birthdate := <optional cal::local_date>$birthdate,
    description := <optional str>$description,
    location := <optional str>$location,
    occupance := <optional str>$occupance
};
