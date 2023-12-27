insert User{
    username := <str>$username,
    first_name := <str>$first_name,
    last_name := <str>$last_name,
    birthdate := <optional cal::local_date>$birthdate,
    email := <str>$email,
    password := <str>$password
}
unless conflict;
