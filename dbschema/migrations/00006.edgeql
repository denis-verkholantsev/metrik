CREATE MIGRATION m13mq7mybkshtdhthvuxirjtvylcow6pv7quotc4ukvxoxkb3ixwoq
    ONTO m1lzz3aaix67pkebkcpcc54lfrhjlryeejah3vcbfkvysuhxh2vvvq
{
  ALTER TYPE default::Skill {
      CREATE MULTI LINK contains: default::Skill;
  };
};
