import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.utils import platform
from kivy.clock import mainthread, Clock

if platform == 'android':
    from jnius import autoclass, PythonJavaClass, java_method
    from android.permissions import request_permissions, Permission

class InterfaceGrafica(BoxLayout):
    def __init__(self, **kwargs):
        super(InterfaceGrafica, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 15

        # 1. Cabeçalho Oficial do seu Projeto
        self.add_widget(Label(text="EDGEOS SOLUTIONS v3.1", font_size=26, size_hint_y=0.15, bold=True, color=(0.1, 0.6, 1, 1)))
        
        self.status = Label(text="Status: Escudo de IA Aguardando Inicialização", color=(1, 0.5, 0, 1), font_size=16, size_hint_y=0.1)
        self.add_widget(self.status)

        # 2. Tela de Telemetria de Hardware (Atualização unificada em tempo real)
        self.layout_hardware = BoxLayout(orientation='vertical', spacing=5, size_hint_y=0.2)
        self.lbl_ram = Label(text="Memória RAM Livre: -- MB", font_size=14)
        self.lbl_temp = Label(text="Temperatura do Chip: -- °C", font_size=14)
        self.layout_hardware.add_widget(self.lbl_ram)
        self.layout_hardware.add_widget(self.lbl_temp)
        self.add_widget(self.layout_hardware)

        # 3. Logs de Diálogo e Ações das IAs
        self.lbl_logs = Label(text="Comunicação das IAs: Aguardando Inicialização...", font_size=12, color=(0.8, 0.8, 0.8, 1), size_hint_y=0.1)
        self.add_widget(self.lbl_logs)

        # 4. Botões Principais de Controle do Usuário
        self.btn_iniciar = Button(text="INICIAR PROTEÇÃO & ESCUDO TÉRMICO", background_color=(0, 1, 0, 1), size_hint_y=0.12, bold=True)
        self.add_widget(self.btn_iniciar)

        self.btn_parar = Button(text="DESATIVAR ESCUDO TEMPORARIAMENTE", background_color=(1, 0, 0, 1), size_hint_y=0.12, bold=True)
        self.btn_parar.disabled = True
        self.add_widget(self.btn_parar)

        # 5. Botão Chave-Mestre: Atualização sob demanda controlada apenas por você
        self.btn_update = Button(text="BUSCAR NOVOS RECURSOS (USO ÚNICO DE REDE)", background_color=(0.5, 0.5, 0.5, 1), size_hint_y=0.1)
        self.add_widget(self.btn_update)

class AntivirusKivyApp(App):
    def build(self):
        self.layout = InterfaceGrafica()
        self.layout.btn_iniciar.bind(on_press=self.acionar_botao_iniciar)
        self.layout.btn_parar.bind(on_press=self.acionar_botao_parar)
        self.layout.btn_update.bind(on_press=self.buscar_atualizacao_segura)
        return self.layout

    def acionar_botao_iniciar(self, instance):
        if platform == 'android':
            self.solicitar_permissoes()
        else:
            self.layout.status.text = "Status: Escudo de IA Ativo & Offline (Simulado)"
            self.layout.status.color = (0, 1, 0, 1)
            self.layout.btn_iniciar.disabled = True
            self.layout.btn_parar.disabled = False

    def solicitar_permissoes(self):
        permissoes = [
            Permission.QUERY_ALL_PACKAGES,
            Permission.REQUEST_DELETE_PACKAGES,
            Permission.READ_SMS,
            Permission.READ_CONTACTS,
            Permission.POST_NOTIFICATIONS,
            Permission.INTERNET
        ]
        request_permissions(permissoes, self.callback_permissoes)

    def callback_permissoes(self, permissions, grants):
        self.ligar_servico_segundo_plano()
        self.escutar_comandos_do_motor()
        
        self.layout.status.text = "Status: Escudo de Inteligência Artificial Ativo & Offline"
        self.layout.status.color = (0, 1, 0, 1)
        self.layout.btn_iniciar.disabled = True
        self.layout.btn_parar.disabled = False
        
        self.notificar_estado_tela(True)

    def ligar_servico_segundo_plano(self):
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        service_class = autoclass('.ServiceAntivirus') 
        self.service_intent = Intent(PythonActivity.mActivity, service_class)
        PythonActivity.mActivity.startForegroundService(self.service_intent)

    def acionar_botao_parar(self, instance):
        if platform == 'android':
            self.notificar_estado_tela(False)
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            if hasattr(self, 'service_intent'):
                PythonActivity.mActivity.stopService(self.service_intent)
        
        self.layout.status.text = "Status: Escudo de IA Desativado"
        self.layout.status.color = (1, 0, 0, 1)
        self.layout.lbl_ram.text = "Memória RAM Livre: -- MB"
        self.layout.lbl_temp.text = "Temperatura do Chip: -- °C"
        self.layout.lbl_logs.text = "Comunicação das IAs: Desconectada."
        self.layout.btn_iniciar.disabled = False
        self.layout.btn_parar.disabled = True

    def notificar_estado_tela(self, esta_visivel):
        if platform == 'android':
            Intent = autoclass('android.content.Intent')
            intent_estado = Intent()
            intent_estado.setAction("com.security.antivirus.ESTADO_INTERFACE")
            intent_estado.putExtra("VISIVEL", esta_visivel)
            self.activity_context.sendBroadcast(intent_estado)

    def buscar_atualizacao_segura(self, instance):
        if platform == 'android':
            Intent = autoclass('android.content.Intent')
            intent_up = Intent()
            intent_up.setAction("com.security.antivirus.TRIGGER_UPDATE")
            intent_up.putExtra("CHAVE_MESTRE", "b4d74c0d2baea38d8d14a39eb3cc1b2930373589b0ec514e50f21e3412241f26")
            self.activity_context.sendBroadcast(intent_up)
            self.layout.lbl_logs.text = "IA Mãe: Sincronizando novos recursos de forma segura..."

    def on_stop(self):
        self.notificar_estado_tela(False)
        super(AntivirusKivyApp, self).on_stop()

    def escutar_comandos_do_motor(self):
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
                acao = intent.getAction()
                
                if acao == "com.security.antivirus.TELEMETRIA_UNIFICADA":
                    ram_livre = intent.getIntExtra("RAM_LIVRE", 0)
                    temp = intent.getFloatExtra("TEMP", 0.0)
                    log_texto = intent.getStringExtra("LOG_TEXTO")
                    
                    self.app.layout.lbl_ram.text = f"Memória RAM Livre: {ram_livre} MB"
                    self.app.layout.lbl_temp.text = f"Temperatura do Chip: {temp} °C"
                    if log_texto:
                        self.app.layout.lbl_logs.text = f"Comunicação das IAs: {log_texto}"
                
                elif acao == "com.security.antivirus.ALERTA_RISCO":
                    nome_app = intent.getStringExtra("APP_NAME")
                    package_name = intent.getStringExtra("PACKAGE_NAME")
                    motivo = intent.getStringExtra("MOTIVO")
                    self.app.exibir_popup_de_risco(nome_app, package_name, motivo)

        self.receptor_ui = ReceptorInterface(self)
        filtro_ui = IntentFilter()
        filtro_ui.addAction("com.security.antivirus.TELEMETRIA_UNIFICADA")
        filtro_ui.addAction("com.security.antivirus.ALERTA_RISCO")
        
        try:
            self.activity_context.registerReceiver(self.receptor_ui, filtro_ui, int(4))
        except Exception:
            self.activity_context.registerReceiver(self.receptor_ui, filtro_ui)

    @mainthread
    def exibir_popup_de_risco(self, nome_app, package_name, motivo):
        layout_alerta = BoxLayout(orientation='vertical', padding=20, spacing=15)
        layout_alerta.add_widget(Label(text=f"AVISO CRÍTICO: {nome_app}", font_size=20, color=(1, 0, 0, 1), bold=True))
        layout_alerta.add_widget(Label(text=motivo, size_hint_y=0.4, text_size=(400, None), halign="center"))
        
        popup = Popup(title="Detecção do Antivírus Offline", content=layout_alerta, size_hint=(0.95, 0.75), auto_dismiss=False)

        btn_remover = Button(text="REMOVER AGORA (RECOMENDADO)", background_color=(0, 1, 0, 1))
        def executing_remocao(instance):
            Uri = autoclass('android.net.Uri')
            Intent = autoclass('android.content.Intent')
            intent_deletar = Intent(Intent.ACTION_UNINSTALL_PACKAGE)
            intent_deletar.setData(Uri.parse(f"package:{package_name}"))
            self.activity_context.startActivity(intent_deletar)
            popup.dismiss()

        btn_remover.bind(on_press=executing_remocao)
        layout_alerta.add_widget(btn_remover)

        btn_ignorar = Button(text="Ignorar ameaça", size_hint_y=0.3, background_color=(0.3, 0.3, 0.3, 1))
        btn_ignorar.bind(on_press=popup.dismiss)
        layout_alerta.add_widget(btn_ignorar)
        popup.open()

if __name__ == '__main__':
    AntivirusKivyApp().run()
