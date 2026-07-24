import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass, PythonJavaClass, java_method
    from android.permissions import request_permissions, Permission
    # Garante a injeção correta de todas as permissões exigidas pelo Android 13
    request_permissions([
        Permission.QUERY_ALL_PACKAGES,
        Permission.REQUEST_DELETE_PACKAGES,
        Permission.READ_SMS,
        Permission.READ_CONTACTS
    ])

class InterfaceGrafica(BoxLayout):
    def __init__(self, **kwargs):
        super(InterfaceGrafica, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20

        # Elementos visuais estruturados do Painel Principal
        self.add_widget(Label(text="SISTEMA DE SEGURANÇA INTEGRADO", font_size=24, size_hint_y=0.2, bold=True))
        self.status = Label(text="Escudo de Inteligência Artificial Ativo & Offline", color=(0, 1, 0, 1), font_size=16)
        self.add_widget(self.status)

class AntivirusKivyApp(App):
    def build(self):
        self.layout = InterfaceGrafica()
        if platform == 'android':
            self.ligar_servico_segundo_plano()
            self.escutar_comandos_do_motor()
        return self.layout

    def ligar_servico_segundo_plano(self):
        """ Ativa a execução estável do arquivo service.py no dispositivo """
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        service_class = autoclass('.ServiceAntivirus') # Nome atribuído no buildozer.spec

        service_intent = Intent(PythonActivity.mActivity, service_class)
        PythonActivity.mActivity.startService(service_intent)

    def escutar_comandos_do_motor(self):
        """ Escuta quando o service.py avisa que um aplicativo perigoso foi instalado """
        IntentFilter = autoclass('android.content.IntentFilter')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        self.activity_context = PythonActivity.mActivity

        class ReceptorInterface(PythonJavaClass):
            __javainterfaces__ = ['android/content/BroadcastReceiver']
            __javacontext__ = 'app'

            def __init__(self, app_instancia):
                super(ReceptorInterface, self).__init__()
                self.app = app_instancia

            @java_method('(Landroid/content/Context;Landroid/content/Intent;)V')
            def onReceive(self, context, intent):
                nome_app = intent.getStringExtra("APP_NAME")
                package_name = intent.getStringExtra("PACKAGE_NAME")
                motivo = intent.getStringExtra("MOTIVO")

                # Executa a exibição da tela de bloqueio e aviso
                self.app.exibir_popup_de_risco(nome_app, package_name, motivo)

        self.receptor_ui = ReceptorInterface(self)
        filtro_ui = IntentFilter("com.security.antivirus.ALERTA_RISCO")
        self.activity_context.registerReceiver(self.receptor_ui, filtro_ui)

    def exibir_popup_de_risco(self, nome_app, package_name, motivo):
        """ Gera a interface visual crítica vermelha que impede o uso sem o consentimento """
        layout_alerta = BoxLayout(orientation='vertical', padding=20, spacing=15)

        layout_alerta.add_widget(Label(text=f"AVISO CRÍTICO: {nome_app}", font_size=20, color=(1, 0, 0, 1), bold=True))
        layout_alerta.add_widget(Label(text=motivo, size_hint_y=0.4, text_size=(400, None), halign="center"))
        layout_alerta.add_widget(Label(text="Deseja manter este aplicativo por sua conta e risco?", size_hint_y=0.2))

        # Criação do Popup bloqueante (auto_dismiss=False impede fechar tocando fora)
        popup = Popup(title="Detecção do Antivírus Offline", content=layout_alerta, size_hint=(0.95, 0.75), auto_dismiss=False)

        # Botão Obrigatório 1: Aciona a rotina nativa para apagar o APK malicioso
        btn_remover = Button(text="REMOVER AGORA (RECOMENDADO)", background_color=(0, 1, 0, 1))
        def executar_remocao(instance):
            Uri = autoclass('android.net.Uri')
            Intent = autoclass('android.content.Intent')
            intent_deletar = Intent(Intent.ACTION_UNINSTALL_PACKAGE)
            intent_deletar.setData(Uri.parse(f"package:{package_name}"))
            self.activity_context.startActivity(intent_deletar)
            popup.dismiss()

        btn_remover.bind(on_press=executar_remocao)
        layout_alerta.add_widget(btn_remover)

        # Botão Obrigatório 2: Usuário assume o risco e fecha o alerta de segurança
        btn_ignorar = Button(text="Ignorar ameaça e assumir as consequências", size_hint_y=0.3, background_color=(0.3, 0.3, 0.3, 1))
        btn_ignorar.bind(on_press=popup.dismiss)
        layout_alerta.add_widget(btn_ignorar)

        popup.open()

if __name__ == '__main__':
    AntivirusKivyApp().run()
    
