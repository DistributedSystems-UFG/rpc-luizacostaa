import rpyc
from constRPYC import *
from rpyc.utils.server import ThreadedServer
from datetime import datetime

class DBList(rpyc.Service):
    value = []

    # --- Logs de conexão ---
    def on_connect(self, conn):
        print(f"[SERVER] Cliente conectado às {datetime.now().strftime('%H:%M:%S')}")

    def on_disconnect(self, conn):
      print(f"[SERVER] Cliente desconectado às {datetime.now().strftime('%H:%M:%S')}")

    def exposed_ping(self):
      return True

    # --- Métodos expostos com logs ---
    def exposed_append(self, data):
        print(f"[SERVER] {datetime.now().strftime('%H:%M:%S')} - append({data})")
        self.value = self.value + [data]
        return self.value
  
    def exposed_insert(self, pos, value):
        MAX_SIZE = 20

        print(f"[SERVER] {datetime.now().strftime('%H:%M:%S')} - insert()")

        # posição inválida (negativa)
        if pos < 0:
            return "❌ A posição não pode ser negativa."

        # posição maior que o limite permitido
        if pos >= MAX_SIZE:
            return f"❌ A posição máxima permitida é {MAX_SIZE - 1}."

        # Preencher com zeros se a posição é maior que o tamanho atual
        zeros_added = 0
        while len(self.value) < pos:
            self.value.append(0)
            zeros_added += 1

        # Agora a posição existe. Inserir deslocando.
        if len(self.value) < MAX_SIZE:
            self.value.insert(pos, value)

            # Se estourou o limite após inserir, remove o último
            if len(self.value) > MAX_SIZE:
                self.value = self.value[:MAX_SIZE]
                return "⚠️ Lista atingiu o tamanho máximo! Último elemento removido automaticamente."

            return self.value
        else:
            return "❌ A lista já está no tamanho máximo e não pode receber novos elementos."

    def exposed_show(self):
        print(f"[SERVER] {datetime.now().strftime('%H:%M:%S')} - show()")
        return self.value

    def exposed_remove(self, pos):
      MAX_SIZE = 20

      print(f"[SERVER] {datetime.now().strftime('%H:%M:%S')} - remove()")

      # posição inválida
      if pos < 0:
          return "❌ A posição não pode ser negativa."

      # posição fora do tamanho atual
      if pos >= len(self.value):
          return f"❌ Não existe elemento na posição {pos}. Tamanho atual: {len(self.value)}."

      # remover o elemento
      removido = self.value.pop(pos)

      return f"Elemento {removido} removido da posição {pos}."

    def exposed_search(self, value):
      print(f"[SERVER] {datetime.now().strftime('%H:%M:%S')} - search({value})")

      # busca por todas as ocorrências
      indices = [i for i, v in enumerate(self.value) if v == value]

      if not indices:
          return f"❌ Valor {value} não encontrado na lista."

      return f"Valor {value} encontrado nas posições: {indices}"

    def exposed_sort(self):
      print(f"[SERVER] {datetime.now().strftime('%H:%M:%S')} - sort()")

      if len(self.value) == 0:
          return "❌ A lista está vazia. Nada para ordenar."

      self.value.sort()
      return self.value

    def exposed_clear(self):
        print(f"[SERVER] {datetime.now().strftime('%H:%M:%S')} - clear()")
        self.value = []
        return self.value


if __name__ == "__main__":
    server = ThreadedServer(DBList(), port=PORT)
    server.start()
