(function(){
    window.Project = Backbone.Model.extend({
        urlRoot: PROJECT_API
    });

    window.Projects = Backbone.Collection.extend({
        urlRoot: PROJECT_API,
        model: Project, 

        maybeFetch: function(options){
            console.log('Projects.maybeFetch');
            // Helper function to fetch only if this collection has not been fetched before.
            if(this._fetched){
                // If this has already been fetched, call the success, if it exists
                options.success && options.success();
                return;
            }

            // when the original success function completes mark this collection as fetched
            var self = this,
                successWrapper = function(success){
                    return function(){
                        self._fetched = true;
                        success && success.apply(this, arguments);
                    };
                };
            options.success = successWrapper(options.success);
            this.fetch(options);
        },

        getOrFetch: function(id, options){
            console.log('Projects.getOrFetch');
            // Helper function to use this collection as a cache for models on the server
            var model = this.get(id);

            if(model){
                options.success && options.success(model);
                return;
            }

            model = new Project({
                resource_uri: id
            });

            model.fetch(options);
        }
        

    });

    window.ProjectView = Backbone.View.extend({
        tagName: 'div',
        className: 'col-6 col-sm-6 col-lg-4',

        events: {
            'click .btn': 'navigate'           
        },

        initialize: function(){
            console.log('ProjectView.initialize');
            this.model.bind('change', this.render, this);
        },

        navigate: function(e){
            console.log('ProjectView.navigate');
            this.trigger('navigate', this.model);
            e.preventDefault();
        },

        render: function(){
            console.log('ProjectView.render');
            $(this.el).html(ich.projectTemplate(this.model.toJSON()));
            return this;
        }                                        
    });


    window.DetailApp = Backbone.View.extend({

        initialize: function(){
            console.log('DetailApp.initialize');
          _.bindAll(this, 'render', 'home', 'saveProject');    
        },

        events: {
            'click .home': 'home',
            'click .save': 'saveProject'
        },
        
        home: function(e){
            console.log('DetailApp.home');
            this.trigger('home');
            e.preventDefault();
        },

        saveProject: function() {
            console.log('DetailApp.saveProject');
            this.model.set({title: this.$("#title").val()});
            this.model.save();
        },

        render: function(){
            console.log('DetailApp.render');
            $(this.el).html(ich.detailApp(this.model.toJSON()));
            return this;
        }                                        
    });

    window.InputView = Backbone.View.extend({
        events: {
            'click .project': 'createProject',
            'keypress #submit': 'createOnEnter'
        },

        createOnEnter: function(e){
            if((e.keyCode || e.which) == 13){
                this.createProject();
                e.preventDefault();
            }

        },

        createProject: function(){
            console.log('click!');
            var title = this.$('#title').val();
            if(title){
                this.collection.create({
                    title: title
                });
                this.$('#title').val('');
            }
        }

    });

    window.ListView = Backbone.View.extend({
        initialize: function(){
            _.bindAll(this, 'addOne', 'addAll');

            this.collection.bind('add', this.addOne);
            this.collection.bind('reset', this.addAll, this);
            this.views = [];
        },

        addAll: function(){
            console.log('ListView.addAll');
            this.views = [];
            this.collection.each(this.addOne);
        },

        addOne: function(project){
            console.log('ListView.addOne');
            var view = new ProjectView({
                model: project
            });
            $(this.el).prepend(view.render().el);
            this.views.push(view);
            view.bind('all', this.rethrow, this);
        },

        rethrow: function(){
            console.log('ListView.rethrow');
            this.trigger.apply(this, arguments);
        }

    });

    window.SingleView = Backbone.View.extend({
        initialize: function(){
            _.bindAll(this, 'addOne', 'addAll');

            this.collection.bind('add', this.addOne);
            this.collection.bind('reset', this.addAll, this);
            this.views = [];
        },

        addAll: function(){
            console.log('ListView.addAll');
            this.views = [];
            this.collection.each(this.addOne);
        },

        addOne: function(project){
            console.log('ListView.addOne');
            var view = new ProjectView({
                model: project
            });
            $(this.el).prepend(view.render().el);
            this.views.push(view);
            view.bind('all', this.rethrow, this);
        },

        rethrow: function(){
            console.log('ListView.rethrow');
            this.trigger.apply(this, arguments);
        }

    });

    window.ListApp = Backbone.View.extend({
        el: "#app",

        rethrow: function(){
            console.log('ListApp.rethrow');
            this.trigger.apply(this, arguments);
        },

        render: function(){
            console.log('ListApp.render');
            $(this.el).html(ich.listApp({}));
            var list = new ListView({
                collection: this.collection,
                el: this.$('#projects')
            });
            list.addAll();
            list.bind('all', this.rethrow, this);
            new InputView({
                collection: this.collection,
                el: this.$('#input')
            });
        }        
    });

    window.SingleApp = Backbone.View.extend({
        el: "#app",

        rethrow: function(){
            console.log('ListApp.rethrow');
            this.trigger.apply(this, arguments);
        },

        render: function(){
            console.log('ListApp.render');
            $(this.el).html(ich.listApp({}));
            var list = new ListView({
                collection: this.collection,
                el: this.$('#projects')
            });
            list.addAll();
            list.bind('all', this.rethrow, this);
            new InputView({
                collection: this.collection,
                el: this.$('#input')
            });
        }        
    });

    
    window.Router = Backbone.Router.extend({
        routes: {
            '': 'list',
            ':id/': 'detail'
        },

        navigate_to: function(model){

            var path = (model && model.get('id') + '/') || '';
            console.log('Router.navigate_to '+path)
            this.navigate(path, true);
        },

        detail: function(){},

        list: function(){}
    });

    $(function(){
        console.log('start here');
        //make a global var app to attatch everything to
        window.app = window.app || {};
        //attatch our custom stuff here
        app.router = new Router();
        app.projects = new Projects();
        //draw outer stuff with templates
        app.list = new ListApp({
            //this thing targets? or extends? things with the ID app
            el: $("#app"),
            //use custom collection from before
            collection: app.projects
        });
        //get ready to draw inner stuff?
        app.detail = new DetailApp({
            el: $("#app")
        });

        app.router.bind('route:list', function(){
            app.projects.maybeFetch({
                success: _.bind(app.list.render, app.list)                
            });
        });
        app.router.bind('route:detail', function(id){
            console.log(app.projects.urlRoot + resource_uri + '/');
            /*
            app.projects.getOrFetch(app.projects.urlRoot + resource_uri + '/', {
                success: function(model){
                    app.detail.model = model;
                    app.detail.render();                    
                }
            });
        */
        });

        //actually do the bindings we just defined
        app.list.bind('navigate', app.router.navigate_to, app.router);
        //app.detail.bind('home', app.router.navigate_to, app.router);
        Backbone.history.start({
            pushState: true, 
            silent: app.loaded
        });
    });
})();