import datetime
from sqlalchemy import *

class MySQLManager:
    def __init__(self, user, password, host, database):
        self.engine = create_engine('mysql+mysqlconnector://'+user+':'+password+'@'+host+'/'+database)
        
        self.meta = MetaData()
        self._setupTables()
        self.meta.create_all(self.engine)
        self.conn = self.engine.connect() 
        
    def _setupTables(self):
        self._setupComuni()
        
        self._setupUtenti()
        
        self._setupAlbum()
        self._setupFoto()
        
        self._setupPost()
        self._setupCommenti()
        
        self._setupPagine()
        self._setupCollegamenti()
        
        self._setupLegami()
        self._setupAmicizie()
        
        self._setupChat()
        self._setupRisposte()
        
    def _setupComuni(self):
        self.comuni = Table('comuni',
                            self.meta,
                            Column('id_comune', Integer, primary_key = True),
                            Column('nome_comune', String)
                            )
    
    def _setupUtenti(self):
        self.utenti = Table('utenti',
                            self.meta,
                            Column('id_utente', Integer, primary_key = True),
                            Column('nome_utente', String),
                            Column('cognome_utente', String),
                            Column('data_nascita_utente', Date),
                            Column('data_iscrizione_utente', DateTime, default=datetime.datetime.utcnow),
                            Column('id_comune_nascita_utente', Integer, ForeignKey('comuni.id_comune')),
                            Column('id_comune_residenza_utente', Integer, ForeignKey('comuni.id_comune'))
                            )
    def _setupAlbum(self):
        self.album = Table('album',
                            self.meta,
                            Column('id_album', Integer, primary_key = True),
                            Column('nome_album', String),
                            Column('id_utente_album', Integer, ForeignKey('utenti.id_utente')),
                            Column('data_creazione_album', DateTime)
                            )
    
    def _setupFoto(self):
        self.foto = Table('foto',
                            self.meta,
                            Column('id_foto', Integer, primary_key = True),
                            Column('id_album_foto', Integer, ForeignKey('album.id_album')),
                            Column('url_foto', String),
                            Column('data_creazione_foto', DateTime)
                            )
        
    
    def _setupPost(self):
        self.post = Table('post',
                            self.meta,
                            Column('id_post', Integer, primary_key = True),
                            Column('id_utente_post', Integer, ForeignKey('utenti.id_utente')),
                            Column('messaggio_post', String),
                            Column('data_creazione_post', DateTime, default=datetime.datetime.utcnow)
                            )
    
    def _setupCommenti(self):
        self.commenti = Table('commenti',
                            self.meta,
                            Column('id_commento', Integer, primary_key = True),
                            Column('id_utente_commento', Integer, ForeignKey('utenti.id_utente')),
                            Column('messaggio', String),
                            Column('data_creazione', DateTime, default=datetime.datetime.utcnow),
                            Column('id_post_commento', Integer, ForeignKey('post.id_post'))
                            )
        
    def _setupPagine(self):
        self.pagine = Table('pagine',
                            self.meta,
                            Column('id_pagina', Integer, primary_key = True),
                            Column('nome_pagina', String),
                            Column('id_utente_pagina', Integer, ForeignKey('utenti.id_utente')),
                            Column('data_creazione_pagina', DateTime, default=datetime.datetime.utcnow)
                            )
    
    def _setupCollegamenti(self):
        self.collegamenti = Table('collegamenti',
                            self.meta,
                            Column('id_collegamento', Integer, primary_key = True),
                            Column('id_pagina_collegamento', Integer, ForeignKey('pagine.id_pagina')),
                            Column('id_utente_collegamento', Integer, ForeignKey('utenti.id_utente')),
                            Column('data_iscrizione_collegamento', DateTime, default=datetime.datetime.utcnow)
                            )
    
    def _setupLegami(self):
        self.legami = Table('legami',
                            self.meta,
                            Column('id_legame', Integer, primary_key = True),
                            Column('id_primo_utente', Integer, ForeignKey('utenti.id_utente')),
                            Column('id_secondo_utente', Integer, ForeignKey('utenti.id_utente'))
                            )
        
    def _setupAmicizie(self):
        self.amicizie = Table('amicizie',
                            self.meta,
                            Column('id_amicizia', Integer, primary_key = True),
                            Column('id_legame_amicizia', Integer, ForeignKey('legami.id_legame')),
                            Column('data_creazione_amicizia', DateTime, default=datetime.datetime.utcnow)
                            )
        
    def _setupChat(self):
        self.chat = Table('chat',
                            self.meta,
                            Column('id_chat', Integer, primary_key = True),
                            Column('id_legame_chat', Integer, ForeignKey('legami.id_legame')),
                            Column('data_creazione_chat', DateTime, default=datetime.datetime.utcnow)
                            )
    
    def _setupRisposte(self):
        self.risposte = Table('risposte',
                            self.meta,
                            Column('id_risposta', Integer, primary_key = True),
                            Column('id_utente_risposta', Integer, ForeignKey('pagine.utenti.id_utente')),
                            Column('messaggio_risposta', String),
                            Column('data_creazione_risposta', DateTime, default=datetime.datetime.utcnow),
                            Column('id_chat_risposta', Integer, ForeignKey('chat.id_chat'))
                            )
    
    def selectFromWhere(self, tablesName, whereCondition):
        sql = select(tablesName).where(whereCondition)
        result = self.conn.execute(sql)
        return result.fetchall()
    
    def insertInto(self, tableName, valuesToInsert):
        sql = insert(tableName).values(valuesToInsert)
        self.conn.execute(sql)
        self.conn.commit()
    
    def deleteFromWhere(self, tableName, whereCondition):
        sql = delete(tableName).where(whereCondition)
        self.conn.execute(sql)
        self.conn.commit()
    
    def updateFromWhere(self, tableName, valuesToUpdate, whereCondition):
        sql = update(tableName).values(valuesToUpdate).where(whereCondition)
        self.conn.execute(sql)
        self.conn.commit()
        
    
        
MyDb = MySQLManager('root', '', '127.0.0.1', 'facebook')

#myQuery = MyDb.selectFromWhere(MyDb.utenti, MyDb.utenti.c.id_utente == 1)
#print(myQuery)

#sqlInsert = MyDb.insertInto(MyDb.comuni, [{'nome_comune': 'Frosinone1'}]);

#sqlUpdate = MyDb.updateFromWhere(MyDb.comuni, {'nome_comune': 'Frosinone'}, MyDb.comuni.c.id_comune == 1)

#sqlDelete = MyDb.deleteFromWhere(MyDb.comuni, MyDb.comuni.c.id_comune == 2)

MyDb.conn.close()
    