@0xadbb7f2622fb11af;

interface Node {
  isDirectory @0 () -> (result :Bool);
}

interface Directory extends(Node) {
  list @0 () -> (list: List(Entry));
  struct Entry {
    name @0 :Text;
    node @1 :Node;
  }

  create @1 (name :Text) -> (file :File);
  mkdir @2 (name :Text) -> (directory :Directory);
  open @3 (name :Text) -> (node :Node);
  delete @4 (name :Text);
  link @5 (name :Text, node :Node);
}

interface File extends(Node) {
  size @0 () -> (size: UInt64);
  read @1 (startAt :UInt64 = 0, amount :UInt64 = 0xffffffffffffffff) -> (data: Data);
  # Default params = read entire file.

  write @2 (startAt :UInt64, data :Data);
  truncate @3 (size :UInt64);
}
