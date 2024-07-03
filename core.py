

import pickle

SAVE_DATA_FILE_NAME = "./save.data"


class Component:
    '''Representação de um componente do sistema'''
    def __init__(self, signature):
        ''' signature: int indica o tipo do componente'''
        self.signature = signature


class EntityComponentSystem:
    '''
    Representa o sistema do jogo.
    signature: int contador das assinaturas dos componentes em potências de 2
    id: int contador dos identificadores do sistema
    scene: Scene cena atual do jogo
    '''
    signature = 1
    id = 0
    scene = None

    @classmethod
    def nextSignature(cls):
        '''
        retorna uma nova assinatura e incrementa o contador para o próximo valor em potência de 2
        return: int a nova assinatura
        '''
        current = cls.signature
        cls.signature = cls.signature << 1
        return current

    @classmethod
    def nextId(cls):
        '''
        retorna um novo id e incrementa o contador para o próximo valor
        return: int o novo identificador
        '''
        cls.id += 1
        return cls.id


class Entity:
    def __init__(self, ECS):
        '''
        id: int identificador único da entidade
        signature: int representa os tipos dos componentes associados utilizando máscara de bits
        components: dict[int, Component] representa todos os componentes do sistema associando a assinatura ao componente
        '''
        self.id = ECS.nextId()
        self.signature = 0
        self.components = dict()

    
    def add(self, component):
        '''
        Adiciona um componente à entidade.
        A assinatura da entidade deve incluir o componente inserido.
        Não é possível inserir um componente já cadastrado.

        component: Component indica o componente a ser associado com a entidade.
        return: Entity a entidade atual após a atualização.
        '''
        if self.has(component.signature):
            raise ValueError()
        self.signature = component.signature | self.signature
        self.components[component.signature] = component
        return self

    
    def remove(self, signature):
        '''
        Remove um componente associado à entidade.
        A assinatura da entidade deve remover o componente especificado pela assinatura.
        Não é possível remover uma assinatura que não está presente.

        signature: int indica a assinatura do componente a ser removido.
        '''
        if not self.has(signature):
            raise ValueError()
        self.signature = self.signature & ~signature
        self.components.pop(signature)

    def has(self, signature):
        '''
        Verifica se a entidade possui um componente para a assinatura especificada.
        singature: int a assinatura a ser consultada.
        return: bool true se a entidade possui um componente para a assinatura especificada e false em caso contrário.
        '''
        return (self.signature & signature) > 0

    def get(self, signature):
        '''
        Recupera o componente para a assinatura especificada.
        Não é possível obter um componente que não está associado.
        singature: int a assinatura a ser consultada
        return: Component o componente associado à assinatura
        '''
        return self.components[signature]

    def __getitem__(self, signature):
        '''
        Recupera o componente para a assinatura especificada usando a notação de acesso por [].
        Não é possível obter um componente que não está associado.
        singature: int a assinatura a ser consultada.
        return: Component o componente associado à assinatura
        '''
        return self.get(signature)

    def __eq__(self, other):
        '''
        Determina se duas entidades são iguais, isto é, se possuem o mesmo id único.
        other: none or Entity entidade sendo comparada
        return: bool true se os objetos são iquais e false em caso contrário
        '''
        return other is not None and self.id == other.id

    def __hash__(self):
        '''
        Determina uma chave hash para o objeto.
        return: int o identificador hash da entidade.
        '''
        return self.id


class Scene:
    def __init__(self):
        '''
        Cria uma nova cena do jogo.
        entities: set[Entity] representa as entidades presentes no jogo.
        '''
        self.entities = set()

    def create(self, entity):
        '''
        Adiciona uma nova entidade ao jogo.
        entity: Entity entidade sendo adicionada
        '''
        self.entities.add(entity)

    def destroy(self, entity):
        '''
        Remove uma entidade do jogo.
        entity: Entity entidade sendo removida.
        '''
        self.entities.remove(entity)

    def filter(self, *signatures):
        '''
        Filtra as entidades do jogo que possuem os componentes indicados pela assinatura considerando a máscara de bits.
        signature: list[int] uma ou mais assinaturas de componentes.
        return: set[Entity] um conjunto de todas as entidades que possuem todos os componentes da assinatura especificada.
        '''
        signature = 0
        for sign in signatures:
            signature = signature | sign
        return set(filter(lambda e: (e.signature & signature) == signature, self.entities))


class Position(Component):
    '''
    Indica que o componente pode ser posicionado no jogo.
    id: int identificador do componente usado na máscara de bits da entidade.
    '''
    id = EntityComponentSystem.nextSignature()

    def __init__(self, x = 0, y = 0):
        '''
        Cria uma nova posição.
        x:int posição na coordenada horizontal limitada entre -4096 a 4096
        y:int posição na coordenada vertical limitada entre -4096 a 4096
        '''
        super().__init__(Position.id)
        if x < -4096 or x > 4096 or y < -4096 or y > 4096:
            raise ValueError()
        self.x = x
        self.y = y

    def __hash__(self):  # grid (-4096, -4096) x (4096, 4096)
        '''
        Determina uma chave hash para o objeto.
        return: int a chave determinada pela expressão 4096 * (4096 + y) + (4096 + x).
        '''
        return 4096 * (4096 + self.y) + (4096 + self.x)

    def __eq__(self, other):
        '''
        Determina se duas posições são iguais em relação às coordenadas.
        other: none or Position a posição sendo comparada.
        return: bool true se as duas posições representam a mesma coordenada e false em caso contrário.
        '''
        return other is not None and self.x == other.x and self.y == other.y



class Renderable(Component):
    '''
    Indica que o componente pode ser desenhado na tela.
    id:int identificador do componente usado na máscara de bits da entidade.
    '''
    id = EntityComponentSystem.nextSignature()

    def __init__(self, glyph, foreground = (255, 255, 255, 255)):
        '''
        glyph: str representação gráfica do componente.
        foreground: tupla[int,int,int,int] a cor utilizada para o desenho
        background: tupla[int,int,int,int] a cor de fundo utilizada para o desenho
        '''
        super().__init__(Renderable.id)
        self.glyph = glyph
        self.foreground = foreground
        self.background = (0, 0, 0, 255)
    
    def draw(self, x, y):
        '''
        Desenha o componente na tela.
        x: int a coordenada horizontal.
        y: int a coordenada vertical.
        '''
        pass



def update(ECS):
    '''
    Atualiza o estado do jogo.
    ECS: EntityComponentSystem sistema.
    '''
    entities = ECS.scene.filter(Position.id | Renderable.id)
    for entity in entities:
        position: Position = entity[Position.id]
        render: Renderable = entity[Renderable.id]
        render.draw(position.x, position.y)



def saveState(filename, ECS):
    '''
    Salva as entidades do jogo em um arquivo.
    filename: str o nome do arquivo.
    ECS: EntityComponentSystem o sistema.
    '''
    data = dict()
    data["entitities"] = ECS.scene.entities
    with open(filename, "wb") as outfile:
        pickle.dump(data, outfile)



def loadState(filename, ECS):
    '''
    Carrega as entidade de um arquivo para o jogo.
    filename: str o nome do arquivo.
    ECS: EntityComponentSystem o sistema.
    '''
    with open(filename, "rb") as infile:
        data = pickle.load(infile)
        ECS.scene.entities = data["entitities"]
