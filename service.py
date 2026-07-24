import os
import time
from kivy.utils import platform                                                    
# Ativa as pontes nativas apenas se estiver rodando no dispositivo Android         if platform == 'android':
    from jnius import autoclass, PythonJavaClass, java_method                      
    # Classes nativas do ecossistema Android para monitorar pacotes
    Context = autoclass('android.content.Context')                                     Intent = autoclass('android.content.Intent')
    IntentFilter = autoclass('android.content.IntentFilter')                           PythonService = autoclass('org.kivy.android.PythonService')

    contexto_servico = PythonService.mService
                                                                                       class CérebroIAVerdadeira:
        """ Esta classe representa o núcleo das suas Inteligências Artificiais Originais """
        def __init__(self):
            # Banco de assinaturas de ameaças carregado na memória local da IA
            self.hashes_maliciosos = [
                "85adecc2a3b04c8104fb17586fa6c9a3528b84d4b29b688c2f1f0a2569d3e8e1",
                "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            ]

        def verificar_comportamento_offline(self, nome_app, tem_sms, tem_contatos):
            """ A IA executa a análise heurística local sem depender de internet """
            # Regra Heurística: Aplicação suspeita tentando acessar dados confidenciais juntos
            if tem_sms and tem_contatos:
                return "PERIGO: Acesso casado a SMS e Contatos detectado de forma suspeita."
            return "SEGURO"

    class OuvinteInstalacaoAndroid(PythonJavaClass):
        """ Escuta nativamente o hardware sempre que um novo APK entra no sistema """
        __javainterfaces__ = ['android/content/BroadcastReceiver']
        __javacontext__ = 'app'

        def __init__(self, ia_instancia):
            super(OuvinteInstalacaoAndroid, self).__init__()
            self.ia = ia_instancia

        @java_method('(Landroid/content/Context;Landroid/content/Intent;)V')
        def onReceive(self, context, intent):
            if intent.getAction() == Intent.ACTION_PACKAGE_ADDED:
                package_name = intent.getData().getSchemeSpecificPart()

                PackageManager = autoclass('android.content.pm.PackageManager')
                Manifest_Permission = autoclass('android.Manifest$permission')
                pm = contexto_servico.getPackageManager()

                try:
                    app_info = pm.getApplicationInfo(package_name, 0)
                    nome_app = str(pm.getApplicationLabel(app_info))

                    # Coleta de dados físicos para entregar à IA Verdadeira
                    pede_sms = pm.checkPermission(Manifest_Permission.READ_SMS, package_name) == PackageManager.PERMISSION_GRANTED
                    pede_contatos = pm.checkPermission(Manifest_Permission.READ_CONTACTS, package_name) == PackageManager.PERMISSION_GRANTED

                    # Executa o julgamento lógico da IA
                    resultado_ia = self.ia.verificar_comportamento_offline(nome_app, pede_sms, pede_contatos)

                    if "PERIGO" in resultado_ia:
                        # Envia uma instrução para o aplicativo principal (main.py) abrir o popup de alerta imediatamente
                        intent_alerta = Intent()
                        intent_alerta.setAction("com.security.antivirus.ALERTA_RISCO")
                        intent_alerta.putExtra("APP_NAME", nome_app)
                        intent_alerta.putExtra("PACKAGE_NAME", package_name)
                        intent_alerta.putExtra("MOTIVO", resultado_ia)
                        contexto_servico.sendBroadcast(intent_alerta)

                except Exception as e:
                    print(f"Erro no processamento do motor da IA: {e}")

    # Inicialização do serviço em segundo plano
    ia_local = CérebroIAVerdadeira()
    receptor = OuvinteInstalacaoAndroid(ia_local)

    filtro = IntentFilter()
    filtro.addAction(Intent.ACTION_PACKAGE_ADDED)
    filtro.addDataScheme("package")
    contexto_servico.registerReceiver(receptor, filter)

# Loop infinito estável para manter o serviço do antivírus vivo no Android
while True:
    time.sleep(1)
