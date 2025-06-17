from collections import defaultdict

class InMemoryDB:
    def __init__(self):
        self.data = [{}]
        self.value_count = [defaultdict(int)]

    def _current_layer(self):
        return self.data[-1], self.value_count[-1]

    def _get_value(self, key):
        for layer in reversed(self.data):
            if key in layer:
                return layer[key]
        return None

    def _update_counts(self, key, new_val, old_val):
        _, count_layer = self._current_layer()
        if old_val is not None:
            count_layer[old_val] -= 1
        if new_val is not None:
            count_layer[new_val] += 1

    def set(self, key, value):
        curr_data, _ = self._current_layer()
        old_value = self._get_value(key)
        curr_data[key] = value
        self._update_counts(key, value, old_value)

    def get(self, key):
        val = self._get_value(key)
        print(val if val is not None else "NULL")

    def unset(self, key):
        curr_data, _ = self._current_layer()
        old_value = self._get_value(key)
        if key in curr_data or old_value is not None:
            curr_data[key] = None
            self._update_counts(key, None, old_value)

    def counts(self, value):
        total = 0
        for count_layer in self.value_count:
            total += count_layer[value]
        print(total)

    def find(self, value):
        found_keys = set()
        seen = set()
        for layer in reversed(self.data):
            for k, v in layer.items():
                if k not in seen:
                    seen.add(k)
                    if v == value:
                        found_keys.add(k)
        for key in found_keys:
            print(key)
        if not found_keys:
            print("NULL")

    def begin(self):
        self.data.append({})
        self.value_count.append(defaultdict(int))

    def rollback(self):
        if len(self.data) == 1:
            print("NO TRANSACTION")
        else:
            self.data.pop()
            self.value_count.pop()

    def commit(self):
        if len(self.data) == 1:
            print("NO TRANSACTION")
            return
        top = self.data.pop()
        top_counts = self.value_count.pop()
        curr = self.data[-1]
        curr_counts = self.value_count[-1]
        for k, v in top.items():
            curr[k] = v
        for k, v in top_counts.items():
            curr_counts[k] += v


def main():
    db = InMemoryDB()
    while True:
        try:
            line = input(" > ").strip()
        except EOFError:
            break
        if not line:
            continue
        parts = line.split()
        cmd = parts[0].upper()
        args = parts[1:]
        if cmd == "END":
            break
        elif cmd == "SET" and len(args) == 2:
            db.set(args[0], args[1])
        elif cmd == "GET" and len(args) == 1:
            db.get(args[0])
        elif cmd == "UNSET" and len(args) == 1:
            db.unset(args[0])
        elif cmd == "COUNTS" and len(args) == 1:
            db.counts(args[0])
        elif cmd == "FIND" and len(args) == 1:
            db.find(args[0])
        elif cmd == "BEGIN":
            db.begin()
        elif cmd == "ROLLBACK":
            db.rollback()
        elif cmd == "COMMIT":
            db.commit()
        else:
            print("INVALID COMMAND")

if __name__ == '__main__':
    main()
