CREATE MIGRATION m1avit3shybanhnfbwuzvqlv2f5xxlh26kguvpl3iyr4caslvliqna
    ONTO m1kjmcxwjypmjfsfiskwx2lkv3xbkih453kbwh5rpmwxhodvt6hgfq
{
  CREATE TYPE default::ExternalLink EXTENDING default::Auditable {
      CREATE LINK user: default::User;
      CREATE REQUIRED PROPERTY url: std::str;
  };
  ALTER TYPE default::User {
      CREATE REQUIRED PROPERTY username: std::str {
          SET REQUIRED USING (<std::str>{});
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE INDEX ON (.username);
      CREATE PROPERTY avatar_url: std::str;
      CREATE PROPERTY description: std::str;
      CREATE PROPERTY location: std::str;
      CREATE PROPERTY occupance: std::str;
  };
};
