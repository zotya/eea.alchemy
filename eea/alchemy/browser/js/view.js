if(window.EEA === undefined){
  var EEA = {
    who: 'eea.alchemy',
    version: '5.0',
  };
}

EEA.Alchemy = function(context, options){
  var self = this;
  self.context = context;

  self.settings = {
    api: 'alchemy.tags.json'
  };

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
}

EEA.Alchemy.prototype = {
  initialize: function(){
    var self = this;
    jQuery.ajax({
        url: self.settings.api,
        success: function(data){
          self.onSuccess(data);
        }
    });
  },

  onSuccess: function(options){
    var self = this;

    // Auto-tagging is not enabled
    if(!options.enabled){
      return;
    }

    // Nothing to search
    if(!(options.search && options.search.length)){
      return;
    }

    jQuery.extend(self.settings, options);
    return self.reload();
  },

  reload: function(){
    var self = this;
    self.context.highlightSearchTerms({
      terms: self.settings.search
    });
  }
};

jQuery.fn.EEAlchemy = function(options){
  return this.each(function(){
    var context = jQuery(this);
    var adapter = new EEA.Alchemy(context, options);
    context.data('EEAlchemy', adapter);
  });
};

// On document ready
jQuery(document).ready(function(){
  items = jQuery('#region-content,#content');
  if(items.length){
    items.EEAlchemy();
  }
});
