import unittest
import pickle
import unittest
from unittest.mock import Mock, call
from unittest.mock import MagicMock, patch
from core import Component, EntityComponentSystem, Entity, Scene, Position, Renderable

class FakeComponent:

    def __init__(self,signature ):
        self.signature = signature
    
class FakeEntityComponentSystem:

    def __init__(self):
        self.signature = 1
        self.id = 0
        self.scene = None
        self.components = {}
        self.entities = {}
        self.masks = {}
        self.systems = []
    
    def nextId(self):
        
        return 1
    
    def nextComponent(self):
        
        return 1
class FakeEntity:

    def __init__(self, ECS):
        self.id = 4
        self.signature = 0
        self.components = 0
    
class FakeScene:
        
        def __init__(self):
            self.entities = []
class FakePosition:
        
        def __init__(self, x, y):
            self.x = 5
            self.y = 10
class FakeRenderable:
            
            def __init__(self, glyph, foreground):
                self.glyph = glyph
                self.foreground = foreground
                self.background = (0, 0, 0, 255)
                self.signature = 3
            def draw(self, x, y):
                pass

class TestComponent(unittest.TestCase):
    # Testes para a classe Component
    def test_init(self):
         # Teste básico para verificar se a inicialização funciona corretamente
        signature = 123
        comp = Component(signature)
        self.assertEqual(comp.signature, signature)
    def test_signature_type(self):
        # Teste para verificar se o tipo de assinatura é int
        signature = 'abc'  # Tipo inválido
        with self.assertRaises(TypeError):
            comp = Component(signature)
    def test_signature_negative(self):
        # Teste para verificar se a assinatura é positiva
        signature = -1  # Tipo inválido
        with self.assertRaises(ValueError):
            comp = Component(signature)

class TestEntityComponentSystem(unittest.TestCase):
    # Testes para a classe EntityComponentSystem
    def setup(self):
        # Inicializa o ambiente de teste
        self.ECS = EntityComponentSystem()
        self.ECS.signature = 1
        self.ECS.id = 0
        self.ECS.scene = None

    def test_nextSignature(self):
        # Teste para verificar se a próxima assinatura é uma potência de 2
        
        self.assertEqual(self.ECS.nextSignature(), 1)
        self.assertEqual(self.ECS.nextSignature(), 2)
        self.assertEqual(self.ECS.nextSignature(), 4)
    def test_nextSignatureReturnType(self):
        # Teste para verificar se a próxima assinatura é um inteiro
        
        self.assertIsInstance(self.ECS.nextSignature(), int)

    def test_NextSignaturePositive(self):
        # Teste para verificar se a próxima assinatura é um inteiro positivo
        self.assertGreater(self.ECS.nextSignature(), 0)
    def test_nextIdReturnType(self):
        # Teste para verificar se o próximo id é um inteiro
        
        self.assertIsInstance(self.ECS.nextId(), int)
    def test_nextIdPositive(self):
        # Teste para verificar se o próximo id é um inteiro positivo
        
        self.assertGreater(self.ECS.nextId(), 0)
    def test_nextId_reset(self):
        # Teste para verificar se o próximo id é incrementado corretamente após a reinicialização
        
        self.ECS.id = 0
        self.assertEqual(self.ECS.nextId(), 1)
        self.assertEqual(self.ECS.id, 1)

    def test_nextId(self):
        # Teste para verificar se o próximo id é um inteiro positivo
        self.assertEqual(self.ECS.nextId(), 1)
        self.assertEqual(self.ECS.nextId(), 2)
        self.assertEqual(self.ECS.nextId(), 3)
    def teardown(self):
        # Limpa o ambiente de teste
        self.ECS = None

class TestEntity(unittest.TestCase):
    # Testes para a classe Entity
    def setup(self):
        # Inicializa o ambiente de teste
        self.ECS = FakeEntityComponentSystem()
        self.ECS.signature = 1
        self.ECS.id = 0
        self.ECS.scene = None
        self.entity = Entity(self.ECS)
    def test_init(self):
        # Teste básico para verificar se a inicialização funciona corretamente
        self.entity = Entity(self.ECS)
        self.assertEqual(self.entity.id, 1)
        self.assertEqual(self.entity.signature, 0)
        self.assertEqual(self.entity.components, {})
    def test_add(self):
        # Teste para verificar se a adição de um componente funciona corretamente
        
        comp = FakeComponent(1)
        self.entity.add(comp)
        self.assertEqual(self.entity.components, {1: comp})
        self.assertEqual(self.entity.signature, 1)
    def test_add_invalid(self):
        # Teste para verificar se a adição de um componente inválido falha
        
        comp = "abc"  # Tipo inválido
        with self.assertRaises(TypeError):
            self.entity.add(comp)
    def test_equal(self):
        # Teste para verificar se duas entidades são iguais
        entity1 = Entity(self.ECS)
        entity2 = Entity(self.ECS)
        self.assertNotEqual(entity1, entity2)
    def test_add_multiple(self):
        # Teste para verificar se a adição de vários componentes funciona corretamente
        entity = Entity(self.ECS)
        comp1 = FakeComponent(1)
        comp2 = FakeComponent(2)
        comp3 = FakeComponent(4)
        entity.add(comp1)
        entity.add(comp2)
        entity.add(comp3)
        self.assertEqual(entity.components, {1: comp1, 2: comp2, 4: comp3})
        self.assertEqual(entity.signature, 3)
    def test_has(self):
        # Teste para verificar se o método has funciona corretamente
        
        comp = FakeComponent(1)
        self.entity.add(comp)
        self.assertTrue(self.entity.has(1))
    def test_has_invalid(self):
        # Teste para verificar se o método has falha com um componente inválido
       
        with self.assertRaises(TypeError):
           self.entity.has("abc")
    def test_has_false(self):
        # Teste para verificar se o método has retorna False corretamente
       
        self.assertFalse(self.entity.has(1))
    def test_remove(self):
        # Teste para verificar se a remoção de um componente funciona corretamente
        
        comp = FakeComponent(1)
        self.entity.add(comp)
        self.entity.remove(1)
        self.assertEqual(self.entity.components, {})
        self.assertEqual(self.entity.signature, 0)
    def test_remove_invalid(self):
        # Teste para verificar se a remoção de um componente inválido falha
        
        with self.assertRaises(ValueError):
            self.entity.remove(1)
    def test_get(self):
        # Teste para verificar se o método get funciona corretamente
        
        comp = FakeComponent(1)
        self.entity.add(comp)
        self.assertEqual(self.entity.get(1), comp)
    def test_get_invalid(self):
        # Teste para verificar se o método get falha com um componente inválido
        
        with self.assertRaises(ValueError):
            self.entity.get(1)
    def test_getitem(self):
        # Teste para verificar se o método getitem funciona corretamente
        
        comp = FakeComponent(1)
        self.entity.add(comp)
        self.assertEqual(self.entity[1], comp)
    def test_getitem_invalid(self):
        # Teste para verificar se o método getitem falha com um componente inválido
       
        with self.assertRaises(ValueError):
            self.entity[1]
    def test_eq(self):
        # Teste para verificar se o método eq funciona corretamente
        entity1 = Entity(self.ECS)
        entity2 = Entity(self.ECS)
        self.assertNotEqual(entity1, entity2)
    def teardown(self):
        # Limpa o ambiente de teste
        self.ECS = None

class TestPosition(unittest.TestCase):
    # Testes para a classe Position
    def test_init_position(self):
        # Teste básico para verificar se a inicialização funciona corretamente
        position = Position(0, 0)
        self.assertEqual(position.x, 0) # Verifica se a posição x foi inicializada corretamente
        self.assertEqual(position.y, 0) # Verifica se a posição y foi inicializada corretamente
    def test_init_position_type(self):
        # Teste para verificar se a posição é um inteiro
        with self.assertRaises(TypeError): # Verifica se a exceção é lançada
            position = Position("a", 0)
        with self.assertRaises(TypeError): # Verifica se a exceção é lançada
            position = Position(0, "a")
    
    def test_limit_position(self):
        #teste para verficar se da erro se digitar uma posição invalida
        with self.assertRaises(ValueError): #verifica se exceção é lançada
            position = Position(-4097, 0)  #testando no valor x maior que 4096
        with self.assertRaises(ValueError): #verifica se exceção é lançada
            position = Position(0, -4097) #testando no valor y maior que 4096
        with self.assertRaises(ValueError): #verifica se exceção é lançada
            position = Position(4097, 0) #testando no valor x maior que 4096
        with self.assertRaises(ValueError): #verifica se exceção é lançada
            position = Position(0, 4097) #testando no valor y maior que 4096

    
class TestScene(unittest.TestCase):
    # Testes para a classe Scene
    def setup(self):
        # Inicializa o ambiente de teste
        self.scene = Scene()
        self.entity = FakeEntity(FakeEntityComponentSystem())
    
    def test_addEntity(self):
        # Teste para verificar se a adição de uma entidade funciona corretamente
        
        self.entity = FakeEntity(FakeEntityComponentSystem())
        self.scene.addEntity(self.entity)
        self.assertEqual(self.scene.entities, [self.entity])
    def test_removeEntity(self):
        # Teste para verificar se a remoção de uma entidade funciona corretamente
        
        entity = FakeEntity(FakeEntityComponentSystem())
        self.scene.addEntity(entity)
        self.scene.removeEntity(entity)
        self.assertEqual(self.scene.entities, [])
    def test_destroy(self):
        # Teste para verificar se a destruição de uma entidade funciona corretamente
        self.scene.addEntity(self.entity)
        self.scene.destroy(self.entity)
        self.assertEqual(self.scene.entities, [])
    def test_filter(self):
        # Teste para verificar se o filtro de entidades funciona corretamente
        self.scene.addEntity(self.entity)
        self.assertEqual(self.scene.filter(1), [self.entity])
    def teardown(self):
        # Limpa o ambiente de teste
        self.scene = None
        self.entity = None

class TestRenderable(unittest.TestCase):
    # Testes para a classe Renderable
    def test_init_renderable(self):
        # Teste básico para verificar se a inicialização funciona corretamente
        renderable = Renderable("a", (255, 255, 255, 255))
        self.assertEqual(renderable.glyph, "a")
        self.assertEqual(renderable.foreground, (255, 255, 255, 255))
        self.assertEqual(renderable.background, (0, 0, 0, 255))
        self.assertEqual(renderable.signature, 3)
    def test_draw(self):
        # Teste para verificar se o método draw funciona corretamente
        renderable = Renderable("a", (255, 255, 255, 255))
        self.assertIsNone(renderable.draw(0, 0))
    def teadown(self):
        # Limpa o ambiente de teste
        self.renderable = None

class TestUpdate(unittest.TestCase):
    def setup(self):
        # Inicializa o ambiente de teste
        self.ECS = FakeEntityComponentSystem()
        self.ECS.signature = 1
        self.ECS.id = 0
        self.ECS.scene = FakeScene()
        self.ECS.scene.entities = []
        self.position = FakePosition(0, 0)
        self.renderable = FakeRenderable("a", (255, 255, 255, 255))
    @patch('path.to.FakeEntityComponentSystem.update')
    def test_update(self,mock_update):
        # Teste para verificar se o método update funciona corretamente
        entity = FakeEntity(self.ECS)
        entity.add(self.position)
        entity.add(self.renderable)
        self.ECS.scene.addEntity(entity)
        self.ECS.update(self.ECS)

        mock_update.assert_called_once_with(self.ECS)
    def teardown(self):
        # Limpa o ambiente de teste
        self.ECS = None
        self.position = None
        self.renderable = None
class TestSaveState(unittest.TestCase,unittest.mock.Mock,unittest.mock.MagicMock,unittest.mock.patch):
    def setup(self):
        # Inicializa o ambiente de teste
        self.ECS = FakeEntityComponentSystem()
        self.ECS.signature = 1
        self.ECS.id = 0
        self.ECS.scene = Scene()
        self.ECS.scene.entities = []
        self.filename = "test.pkl"
        
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("pickle.dump")
    def test_saveState(self,mock_open,mock_pickle_dump):
        # Teste para verificar se o método saveState funciona corretamente
        entity = FakeEntity(self.ECS)
        self.ECS.scene.addEntity(entity)
        # Salva o estado do jogo
        self.ECS.saveState(self.filename, self.ECS)
        # Verifica se o arquivo foi aberto corretamente
        mock_open.assert_called_once_with(self.filename, "wb")
        #Verifica se pickle.dump foi chamado corretamente
        mock_pickle_dump.assert_called_once()
    def teardown(self):
        # Limpa o ambiente de teste
        self.ECS = None
        self.filename = None
class TestLoadState(unittest.TestCase,unittest.mock.Mock,unittest.mock.MagicMock,unittest.mock.patch):
    def setup(self):
        # Inicializa o ambiente de teste
        self.ECS = FakeEntityComponentSystem()
        self.ECS.signature = 1
        self.ECS.id = 0
        self.ECS.scene = FakeScene()
        self.ECS.scene.entities = []
        self.filename = "test.pkl"
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("pickle.load")
    def test_loadState(self,mock_pickle_load, mock_open):
        # Teste para verificar se o método loadState funciona corretamente
        entity = FakeEntity(self.ECS)

        self.ECS.scene.addEntity(entity)
        
        # dados simulados
        data = {"entities": self.ECS.scene.entities}

        self.ECS.loadState(self.filename, self.ECS)
        
        # Verifica se o arquivo foi aberto corretamente
        mock_open.assert_called_once_with(self.filename, "rb")
        
        # Verifica se pickle.load foi chamado corretamente
        mock_pickle_load.assert_called_once()
        
        # Verifica se as entidades foram carregadas corretamente
        self.assertEqual(self.ECS.scene.entities, data["entities"])
    def teardown(self):
        # Limpa o ambiente de teste
        self.ECS = None
        self.filename = None
    
class TestComponentSystem(unittest.TestCase):
    # Testes para a classe EntityComponentSystem
    def setUp(self): # Inicializa o ambiente de teste
        self.ECS = FakeEntityComponentSystem()
        self.ECS.signature = 1
        self.ECS.id = 0
        self.ECS.scene = []
    def test_nextId(self): # Testa o método nextId
        self.assertEqual(self.ECS.nextId(), 1)
    def test_nextComponent(self): # Testa o método nextComponent
        self.assertEqual(self.ECS.nextComponent(), 1)
    def test_nextSignature(self): # Testa o método nextSignature
        self.assertEqual(self.ECS.nextSignature(), 4)
    def test_Entity(self): # Testa a classe Entity
        entity = self.ECS.Entity()
        self.assertEqual(entity.components, {})

    def test_init(self): # Testa o método __init__
        
        self.assertEqual(self.ECS.scene, [])
        self.assertEqual(self.ECS.components, {})
        self.assertEqual(self.ECS.entities, {})
        self.assertEqual(self.ECS.masks, {})
        self.assertEqual(self.ECS.systems, [])
    def test_addComponent(self): # Testa o método addComponent
        
        component = FakeComponent("a", (255, 255, 255, 255))
        self.ECS.addComponent(component)
        self.assertEqual(self.ECS.components, {1: component})
    def test_addEntity(self): # Testa o método addEntity
       
        entity = FakeEntityComponentSystem.Entity()
        self.ECS.addEntity(entity) # Adiciona a entidade ao sistema
        self.assertEqual(self.ECS.entities, {1: entity})
    def test_addSystem(self): # Testa o método addSystem
        
        def f():
            pass
        self.ECS.addSystem(f)
        self.assertEqual(self.ECS.systems, [f])
    def test_filter(self): # Testa o método filter
        
        component = FakeComponent("a", (255, 255, 255, 255))
        self.ECS.addComponent(component)
        entity = FakeEntityComponentSystem.Entity()
        entity.addComponent(component)
        self.ECS.addEntity(entity)
        self.assertEqual(self.ECS.filter(1), [entity])
    
    def tearDown(self): # Limpa o ambiente de teste
        self.ECS = None

    
    
        
if __name__ == "__main__":
    unittest.main()