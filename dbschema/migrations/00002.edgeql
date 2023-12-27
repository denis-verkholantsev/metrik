CREATE MIGRATION m1kjmcxwjypmjfsfiskwx2lkv3xbkih453kbwh5rpmwxhodvt6hgfq
    ONTO m17s457wapiwoq4oqyn5qxa2smtz7bc6l4btoz64qc2mkfnygelg3a
{
  ALTER TYPE default::User {
      ALTER PROPERTY email {
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
